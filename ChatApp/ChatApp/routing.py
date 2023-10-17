# your_project/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middleware import WebSocketAuthMiddleware
import chat.routing

application = ProtocolTypeRouter(
    {
        "websocket": WebSocketAuthMiddleware(
            URLRouter(chat.routing.websocket_urlpatterns)
        ),
    }
)
