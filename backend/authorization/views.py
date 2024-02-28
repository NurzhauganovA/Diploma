from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User


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
        return redirect('login')

    return render(request, 'authorization/register.html')


def logout(request):
    return render(request, 'logout.html')
