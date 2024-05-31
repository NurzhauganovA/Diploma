from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import Notification


def send_notification(sender, receiver, title, message):
    notification = Notification.objects.create(
        from_who=sender,
        to_who=receiver,
        title=title,
        body=message
    )
    print(f'Notification created: {notification}')

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        {
            'message': message
        }
    )
    print(f'Notification sent')


def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_who=user, is_read=False).order_by('-created_at')

    return notifications


class GetNotifications(APIView):
    def get(self, request):
        notifications = get_notifications(request)

        return Response({
            'notifications': [
                {
                    'id': notification.id,
                    'from_who': notification.from_who.mobile_phone,
                    'title': notification.title,
                    'body': notification.body,
                    'created_at': notification.created_at
                } for notification in notifications
            ]
        })
