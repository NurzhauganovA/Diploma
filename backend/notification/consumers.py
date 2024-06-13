import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
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

        # await self.send(text_data=json.dumps({
        #     'type': 'chat_message',
        #     'message': 'Пользователь покинул чат'
        # }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))
