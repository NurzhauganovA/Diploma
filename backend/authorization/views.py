import json

from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import User
from .services import random_generated_code


def login(request):
    if request.method == 'POST':
        mobile_phone = request.POST.get('mobile_phone')
        password = request.POST.get('password')

        user = User.objects.filter(mobile_phone=mobile_phone).first()

        if user is None:
            messages.error(request, 'User with this phone number does not exist!')
            return redirect('login')

        if user.password != password:
            messages.error(request, 'Password is incorrect!')
            return redirect('login')

        return redirect('/')
    return render(request, 'authorization/login.html')


def register(request):
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

        User.objects.create(
            full_name=full_name,
            mobile_phone=mobile_phone,
            role=role,
            password=password
        )

        messages.success(request, 'User created successfully!')
        return redirect('enter-email')

    return render(request, 'authorization/register.html')


def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = random_generated_code(email)
        send_mail(
            subject='SmartSchool - Verify email',
            message=f'Your verification code is: {code}',
            from_email='',
            recipient_list=[email],
        )

        return redirect('verify-email')
    return render(request, 'authorization/enter_email.html')


def verify_email(request):
    if request.method == 'POST':
        verification_code = json.loads(request.body).get('verification_code')

        return JsonResponse({'message': 'Email verified successfully!', 'verification_code': verification_code})
    return render(request, 'authorization/verify_email.html')


def logout(request):
    return render(request, 'logout.html')
