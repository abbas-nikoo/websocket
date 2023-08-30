# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import GroupChat, ChatMessage
# from channels.db import database_sync_to_async
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.show_previous_messages = True
#
#     async def connect(self):
#         self.group_name = self.scope['url_route']['kwargs']['group_name']
#         self.group = await self.get_or_create_group(self.group_name)
#
#         headers = self.scope.get('headers', [])
#         session_key = None
#
#         for header, value in headers:
#             if header.decode('utf-8') == 'sessionkey':
#                 session_key = value.decode('utf-8')
#
#         if not session_key:
#             await self.close()  # قطع اتصال
#
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#         if self.show_previous_messages:
#             await self.send_previous_messages()
#             self.show_previous_messages = False
#
#             # ارسال پیام به گروه که کاربر وارد شده است
#             await self.send_status_message('connected')
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#
#         # ارسال پیام به گروه که کاربر خارج شده است
#         await self.send_status_message('disconnected')
#
#     async def send_status_message(self, status, session_key=None):
#         session_key = await self.get_session_key()
#         status_message = f"{status}."
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'session_key': session_key,
#                 'message': status_message,
#                 'status': status
#             }
#         )
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get('message', '')
#         # status = data.get('status')
#
#         headers = self.scope.get('headers', [])
#         session_key = None
#
#         for header, value in headers:
#             if header.decode('utf-8') == 'sessionkey':
#                 session_key = value.decode('utf-8')
#
#         # اگر sessionKey خالی نبود، پیام را ارسال کن
#         if session_key:
#
#             await self.save_message(session_key, message)
#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     'type': 'chat_message',
#                     'session_key': session_key,
#                     'message': message,
#                 }
#             )


import json
import os.path

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, ChatMessage, ImageMessage
from channels.db import database_sync_to_async
import base64
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile



def base64_to_image(image_base64):
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))


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
            await self.close()

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        if self.show_previous_messages:
            await self.send_previous_messages()
            self.show_previous_messages = False
            await self.send_status_message('connected')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
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

    async def handle_hand_raise(self, event):
        session_key = event.get('session_key', '')

        if session_key:
            await self.send(text_data=json.dumps({
                'hand_raise': True,
                'session_key': session_key,
            }))

    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message = data.get('message', '')
    #     status = data.get('status')
    #
    #     headers = self.scope.get('headers', [])
    #     session_key = None
    #
    #     for header, value in headers:
    #         if header.decode('utf-8') == 'sessionkey':
    #             session_key = value.decode('utf-8')
    #
    #     if session_key:
    #         if status == 'typing':
    #             await self.channel_layer.group_send(
    #                 self.group_name,
    #                 {
    #                     'type': 'handle_typing',
    #                     'session_key': session_key,
    #                     'status': status,
    #                 }
    #             )
    #         elif status == 'hand_raise':
    #             await self.channel_layer.group_send(
    #                 self.group_name,
    #                 {
    #                     'type': 'handle_hand_raise',
    #                     'session_key': session_key,
    #                 }
    #             )
    #         else:
    #             await self.save_message(session_key, message)
    #             await self.channel_layer.group_send(
    #                 self.group_name,
    #                 {
    #                     'type': 'chat_message',
    #                     'session_key': session_key,
    #                     'message': message,
    #                 }
    #             )
    #
    # # ... دیگر متدها به همان شکل که بالا توضیح داده شده‌اند.


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        status = data.get('status')
        image_base64 = data.get('image', '')  # دریافت تصویر به صورت Base64

        headers = self.scope.get('headers', [])
        session_key = None

        for header, value in headers:
            if header.decode('utf-8') == 'sessionkey':
                session_key = value.decode('utf-8')

        # if session_key:

        if image_base64:
            await self.save_image(session_key, image_base64)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_image',
                    'session_key': session_key,
                    'image': image_base64,
                }
            )
        else:
            if status == 'typing':
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'handle_typing',
                        'session_key': session_key,
                        'status': status,
                    }
                )
            elif status == 'hand_raise':
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'handle_hand_raise',
                        'session_key': session_key,
                    }
                )
            else:
                await self.save_message(session_key, message)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'session_key': session_key,
                        'message': message,
                    }
                )

    # @database_sync_to_async
    # def convert_image_to_base64(self, image_path):
    #     with open(image_path, "rb") as image_file:
    #         base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    #     return base64_encoded_image

    @database_sync_to_async
    def save_image(self, session_key, image_base64):
        try:
            image = base64_to_image(image_base64)
            image = image.convert("RGB")  # تبدیل تصویر به حالت RGB

            # انجام تغییر اندازه بر روی تصویر
            image.thumbnail((800, 800), Image.LANCZOS)

            # ذخیره تصویر در دیتابیس
            image_filename = os.path.join('media', f"{session_key}.jpg")
            output = BytesIO()
            image.save(output, format='JPEG', quality=70)
            image_message = ImageMessage(group=self.group, session_key=session_key)
            image_message.image.save(image_filename, InMemoryUploadedFile(output, None,  "%s.jpg" %
            image_filename.split('/')[
                -1], 'image/jpeg', sys.getsizeof(output), None), save=False)
            image_message.save()
        except Exception as e:
            print(f"Error saving image: {str(e)}")

    # @database_sync_to_async
    # def save_image(self, session_key, image_base64):
    #     try:
    #         image = base64_to_image(image_base64)
    #         # image = image.convert("RGB")
    #         image_filename = os.path.join('media', f"{session_key}.jpg")
    #
    #         # ذخیره تصویر در دیتابیس
    #         image_message = ImageMessage(group=self.group, session_key=session_key)
    #         image_message.image.save(image_filename, image, save=False)
    #         image_message.save()
    #     except Exception as e:
    #         print(f"Error saving image: {str(e)}")
    async def send_image(self, event):
        image_base64 = event['image']
        session_key = event.get('session_key', '')

        if session_key:
            await self.send(text_data=json.dumps({
                'image': image_base64,
                'session_key': session_key,
            }))



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

    # async def send_previous_messages(self):
    #     previous_messages = await self.get_previous_messages(self.group)
    #     for message in previous_messages:
    #         await self.send(text_data=json.dumps({
    #             'message': message.message,
    #             'session_key': message.session_key,
    #         }))

    async def send_previous_messages(self):
        previous_messages = await self.get_previous_messages(self.group)
        previous_image_messages = await self.get_previous_image_messages(self.group)

        for message in previous_messages:
            await self.send(text_data=json.dumps({
                'message': message.message,
                'session_key': message.session_key,
            }))

            for image_message in previous_image_messages:
                await self.send(text_data=json.dumps({
                    'image': image_message.image.url,  # ارسال آدرس تصویر به کاربر
                    'session_key': image_message.session_key,
            }))

    @database_sync_to_async
    def get_or_create_group(self, group_name):
        group, _ = GroupChat.objects.get_or_create(group_name=group_name)
        return group

    @database_sync_to_async
    def get_previous_image_messages(self, group):
        previous_image_messages = ImageMessage.objects.filter(group=group).order_by('timestamp')
        return list(previous_image_messages)

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
