import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None

    async def connect(self):
        self.group_name = 'notification'

        # join to group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        await self.close()

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': 'Пользователь покинул чат'
        }))

    async def receive(self, **kwargs):
        text_data = json.loads(kwargs.get('text_data'))
        message = text_data['message']

        event = {
            'type': 'chat_message',
            'message': message
        }

        # send message to group
        await self.channel_layer.group_send(
            self.group_name,
            event
        )

        await self.send(text_data=json.dumps(event))

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))
