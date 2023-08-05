<<<<<<< HEAD
# from django.urls import re_path
#
# from . import consumers
#
# websocket_urlpatterns = [
#     re_path(r"ws/chat/(?P<group_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
# ]
=======
# routing.py
from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
]
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825
