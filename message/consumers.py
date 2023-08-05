import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.group_name = self.scope['url_route']['kwargs']['group_name']
            self.group = await self.get_or_create_group(self.group_name)
        except Exception as e:
            print(str(e))

        # اتصال به گروه
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # قطع اتصال از گروه
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.dumps(text_data)

        # Send message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def chat_message(self, event):
        message = event['message']

        # ارسال پیام به کلاینت‌ها
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    @staticmethod
    async def get_or_create_group(group_name):
        group, _ = await GroupChat.objects.get_or_create(group_name=group_name)
        return group

    @staticmethod
    async def save_message(group, sender, message):
        chat_message = ChatMessage(group=group, sender=sender, message=message)
        await chat_message.save()
