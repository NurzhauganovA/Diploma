import json
import cv2
import face_recognition
import numpy as np

from django.contrib import messages, auth
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.http.request import HttpRequest

from authorization import UserRoles
from authorization.models import User
from authorization.utils import send_email, verify_account


def login(request: HttpRequest):
    if request.method == 'POST':
        mobile_phone = request.POST.get('mobile_phone')
        password = request.POST.get('password')

        user: User = User.objects.filter(mobile_phone=mobile_phone).first()
        print(mobile_phone)

        if user is None:
            messages.error(request, 'User with this phone number does not exist!')
            return redirect('login')

        if not user.check_password(password):
            messages.error(request, 'Password is incorrect!')
            return redirect('login')

        if user.role == UserRoles.EMPLOYEE:
            face_control(user)
            # if face_control(user) != user.full_name:
            #     return JsonResponse({"error": "THERE IS ERROR"})

        auth.login(request, user)
        user.save_login_days()

        return redirect('/')

    return render(request, 'authorization/login.html')


def register(request: HttpRequest):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_phone = request.POST.get('mobile_phone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(mobile_phone=mobile_phone).exists():
            messages.error(request, 'User with this phone number already exists!')
            return redirect('register')

        new_user = User.objects.create(
            full_name=full_name,
            mobile_phone=mobile_phone,
            role=role,
            password=password
        )

        messages.success(request, 'User created successfully!')

        request.session['mobile_phone'] = mobile_phone
        request.session['password'] = password

        return redirect('enter-email')

    return render(request, 'authorization/register.html')


def enter_email(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')

        send_email(
            email=email,
            subject='SmartSchool - Verify email',
            message='Your verification code'
        )

        request.session['email'] = email

        return redirect('verify-email')

    return render(request, 'authorization/enter_email.html')


def verify_email(request: HttpRequest):
    mobile_phone = request.session.get('mobile_phone')
    password = request.session.get('password')
    email = request.session.get('email')

    if request.method == 'POST':
        body = json.loads(request.body)
        code = body.get('verification_code')

        if verify_account(email=email, code=int(code)):
            user = User.objects.filter(mobile_phone=mobile_phone).first()
            user.email = email
            user.save()

            if not user.check_password(password):
                return JsonResponse({'message': 'Password is incorrect!', 'status': 400})

            auth.login(request, user)
            user.save_login_days()

            return JsonResponse({'message': 'User verified successfully!', 'status': 200})

        return JsonResponse({'message': 'Verification code is incorrect!', 'status': 400})

    return render(request, 'authorization/verify_email.html', {'email': email})


def logout(request: HttpRequest):
    return render(request, 'logout.html')


def forgot_password(request: HttpRequest):

    if request.method == "POST":
        email = request.POST.get("email")

        send_email(
            email=email,
            subject="SmartSchool - Reset password",
            message="Your verification code"
        )

        request.session['email'] = email

        return redirect("verify-by-code")
    
    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def verify_by_code(request: HttpRequest):

    if request.method == "POST":
        email = request.session.get("email")
        body = json.loads(request.body)
        code = body.get('verification_code')

        if verify_account(email, code):
            return redirect("set-password")
        
        return JsonResponse({'message': 'Verification code is incorrect!', 'status': 400})
    
    return JsonResponse({"error": "Not Allowed Method", "status": 405})



def set_new_password(request: HttpRequest):
    
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('set-password')
        
        user: User = User.objects.get(email=request.session.get("email"))

        user.set_password(password)
        
        return redirect("login")
    
    return JsonResponse({"error": "Not Allowed Method", "status": 405})


def face_control(user: User):

    # video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    video_capture = cv2.VideoCapture(0)

    image = face_recognition.load_image_file(user.user_info.photo_avatar)
    image_encoding = face_recognition.face_encodings(image)[0]

    know_face_encodings = [image_encoding]
    know_face_names = [user.full_name]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:

                matches = face_recognition.compare_faces(know_face_encodings, face_encoding)
                name = "Unkown"

                face_distances = face_recognition.face_distance(know_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = know_face_names[best_match_index]

                face_names.append(name)
        
        process_this_frame = not process_this_frame
        # return face_names[0]
    
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return face_names[0]