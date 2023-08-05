import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
<<<<<<< HEAD
# from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from message import consumers

# from message.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    # "websocket": AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    # ),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<group_name>/', consumers.ChatConsumer.as_asgi()),
        ]))

=======
from message.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
>>>>>>> 866b8290fbb0226912cd8cd1b9ae58053e5d1825
})
