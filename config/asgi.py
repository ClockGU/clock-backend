import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path

from config.consumers import MyConsumer
from config.middleware import JWTAuthMiddleware

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()  # Ensure Django is fully initialized

# WebSocket routing with your middleware
websocket_application = JWTAuthMiddleware(
    AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/reportsocket/", MyConsumer.as_asgi()),
            ]
        )))

# Define the overall ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websocket_application,
})
