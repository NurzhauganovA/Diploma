from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('enter-email/', views.enter_email, name='enter-email'),
    path('verify-email/', views.verify_email, name='verify-email'),
]
