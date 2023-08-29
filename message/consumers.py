import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, ChatMessage
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_previous_messages = True

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group = await self.get_or_create_group(self.group_name)

        headers = self.scope.get('headers', [])
        session_key = None

        for header, value in headers:
            if header.decode('utf-8') == 'sessionkey':
                session_key = value.decode('utf-8')

        if not session_key:
            await self.close()  # قطع اتصال

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        if self.show_previous_messages:
            await self.send_previous_messages()
            self.show_previous_messages = False

            # ارسال پیام به گروه که کاربر وارد شده است
            await self.send_status_message('connected')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        # ارسال پیام به گروه که کاربر خارج شده است
        await self.send_status_message('disconnected')

    async def send_status_message(self, status, session_key=None):
        session_key = await self.get_session_key()
        status_message = f"{status}."
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'session_key': session_key,
                'message': status_message,
                'status': status
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        # status = data.get('status')

        headers = self.scope.get('headers', [])
        session_key = None

        for header, value in headers:
            if header.decode('utf-8') == 'sessionkey':
                session_key = value.decode('utf-8')

        # اگر sessionKey خالی نبود، پیام را ارسال کن
        if session_key:

            await self.save_message(session_key, message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'session_key': session_key,
                    'message': message,
                }
            )

    @database_sync_to_async
    def save_message(self, session_key, message):
        chat_message = ChatMessage(group=self.group, session_key=session_key, message=message)
        chat_message.save()

    async def chat_message(self, event):
        message = event['message']
        session_key = event.get('session_key', '')

        if session_key:
            await self.send(text_data=json.dumps({
                'message': message,
                'session_key': session_key,
                }))

    async def send_previous_messages(self):
        previous_messages = await self.get_previous_messages(self.group)
        for message in previous_messages:
            await self.send(text_data=json.dumps({
                'message': message.message,
                'session_key': message.session_key,
            }))

    @database_sync_to_async
    def get_or_create_group(self, group_name):
        group, _ = GroupChat.objects.get_or_create(group_name=group_name)
        return group

    @database_sync_to_async
    def get_previous_messages(self, group):
        previous_messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
        return list(previous_messages)

    async def get_session_key(self):
        headers = self.scope.get('headers', [])

        for header, value in headers:
            if header.decode('utf-8') == 'sessionkey':
                return value.decode('utf-8')
        return None
