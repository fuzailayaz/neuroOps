"""
WebSocket routing configuration for the NeuroOps project.
"""
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django.core.asgi import get_asgi_application

# Import WebSocket consumers here
from chat.consumers import ChatConsumer

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# WebSocket URL patterns
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})
