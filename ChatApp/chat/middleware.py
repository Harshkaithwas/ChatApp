from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract the access token from the query parameters or headers
        query_string = scope.get("query_string", b"").decode("utf-8")
        token = None

        if "token=" in query_string:
            token = query_string.split("token=")[1]
        else:
            headers = dict(scope["headers"])
            if b"authorization" in headers:
                auth_header = headers[b"authorization"].decode("utf-8")
                if auth_header.startswith("Token "):
                    token = auth_header.split("Token ")[1]

        # Authenticate the user based on the access token
        if token:
            try:
                user = Token.objects.get(key=token).user
            except Token.DoesNotExist:
                user = AnonymousUser()
        else:
            user = AnonymousUser()

        # Set the authenticated user to the scope
        scope["user"] = user

        return await super().__call__(scope, receive, send)
