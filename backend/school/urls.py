from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.get_people, name='get_people'),
    # path('user/<int:user_id>/', views.user_detail, name='user_detail'),
]
