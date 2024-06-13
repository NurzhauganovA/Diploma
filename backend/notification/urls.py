from django.urls import path
from notification.views import GetNotifications


urlpatterns = [
    path("get/", GetNotifications.as_view(), name="get_notifications")
]
