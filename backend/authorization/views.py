import json

from django.contrib import messages, auth
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http.request import HttpRequest

from .models import User
from .utils import send_email, verify_account, send_link


def login(request: HttpRequest):
    if request.method == 'POST':
        mobile_phone = request.POST.get('mobile_phone')
        password = request.POST.get('password')

        user: User = User.objects.filter(mobile_phone=mobile_phone).first()

        if user is None:
            messages.error(request, 'User with this phone number does not exist!')
            return redirect('login')

        if not user.check_password(password):
            messages.error(request, 'Password is incorrect!')
            return redirect('login')

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
