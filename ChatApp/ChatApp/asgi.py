# your_project_name/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat import consumers  # Import your consumers
from channels.auth import AuthMiddlewareStack
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatApp.settings")

# Add this line to apply the WebSocketAuthMiddleware
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # For handling HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
            # Add more WebSocket URL patterns if needed
        ])
    ),
    # Add other routing for other protocols here, if needed
})
