from django.http import HttpResponse
from django.shortcuts import render, redirect


def main(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')

    return redirect('login')
