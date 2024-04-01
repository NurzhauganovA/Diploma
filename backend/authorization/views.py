import json

from django.contrib import messages, auth
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import User
from .utils import send_email, verify_account


def login(request):
    if request.method == 'POST':
        mobile_phone = request.POST.get('mobile_phone')
        password = request.POST.get('password')

        user = User.objects.filter(mobile_phone=mobile_phone).first()

        if user is None:
            messages.error(request, 'User with this phone number does not exist!')
            return redirect('login')

        if not user.check_password(password):
            messages.error(request, 'Password is incorrect!')
            return redirect('login')

        auth.login(request, user)

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


def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        cache_email = send_email(
            email=email,
            subject='SmartSchool - Verify email',
            message='Your verification code'
        )

        request.session['email'] = cache_email

        return redirect('verify-email')

    return render(request, 'authorization/enter_email.html')


def verify_email(request):
    mobile_phone = str(request.session.get('mobile_phone'))
    password = str(request.session.get('password'))
    email = str(request.session.get('email'))

    context = {
        'email': email
    }

    if request.method == 'POST':
        body = json.loads(request.body)
        code = body.get('verification_code')

        if verify_account(email=email, code=code):
            user = User.objects.filter(mobile_phone=mobile_phone).first()
            user.email = email
            user.save()

            auth.login(request, user)

            return JsonResponse({'message': 'User verified successfully!', 'status': 200})

        return JsonResponse({'message': 'Verification code is incorrect!', 'status': 400})

    return render(request, 'authorization/verify_email.html', context)


def logout(request):
    return render(request, 'logout.html')
