from django.urls import path
from . import views

urlpatterns = [
    path('school-part', views.school_part, name='school-part'),

    path("schools/<int:pk>/", views.get_people, name="get_people"),
    path("users/<int:pk>/", views.get_more_info, name="get_more_info"),
]
