import json
import cv2 as cv
import face_recognition as face_rec
import numpy as np

from django.contrib import messages, auth
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.urls import reverse

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
            request.session["employee_id"] = user.id

            # return redirect("face_recognition")
            return render(request, "authorization/face_control.html")

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


def face_recognize(request: HttpRequest):
    id = request.session["employee_id"]
    user = User.objects.get(id=id)

    if face_control(user.full_name):
        auth.login(request, user)
        user.save_login_days()

        return JsonResponse({"redirect": reverse("home"), "code": 302})

    return JsonResponse(
        {'message': 'Forbidden', 
         "code": 403, 
         "info": "Facial recognition failed", 
         "button": "Please go back to login",
         "redirect": reverse("error"),
         "link": "login",
         }
    )


def face_control(user_name: str):
    video_capture = cv.VideoCapture(0)

    users = User.objects.all()
    know_face_encodings, know_face_names = [], []

    for user in users:
        if hasattr(user, "user_info") and user.user_info.photo_avatar:
            image = face_rec.load_image_file(user.user_info.photo_avatar)
            image_encoding = face_rec.face_encodings(image)[0]
            know_face_encodings.append(image_encoding)
            know_face_names.append(user.full_name)


    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        _, frame = video_capture.read()

        if process_this_frame:
            small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_rec.face_locations(rgb_small_frame)
            face_encodings = face_rec.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:

                matches = face_rec.compare_faces(know_face_encodings, face_encoding, tolerance=0.39)
                name = "Unkown"

                face_distances = face_rec.face_distance(know_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = know_face_names[best_match_index]

                print("CHECK:", face_distances, best_match_index, matches)
                face_names.append(name)
        
        process_this_frame = not process_this_frame

        if len(face_names) > 0:
            break

    result = face_names[0] == user_name
    return result


def errorViews(request: HttpRequest):
    code = request.GET.get("code")
    message = request.GET.get("message")
    info = request.GET.get("info")
    button = request.GET.get("button")
    link = request.GET.get("link")

    context = {
        "code": code,
        "message": message,
        "info": info,
        "button": button,
        "link": link,
    }

    return render(request, "authorization/error.html", context)