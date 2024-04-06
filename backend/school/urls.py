from django.urls import path
from . import views

urlpatterns = [
    path("schools/<int:pk>/", views.get_people, name="get_people"),
    path("users/<int:pk>/", views.get_more_info, name="get_more_info"),
]
