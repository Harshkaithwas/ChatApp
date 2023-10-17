from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from . import consumers  # Import your consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
        # Add more WebSocket URL patterns if needed
    ]),
    # Add other routing for other protocols here, if needed
})
