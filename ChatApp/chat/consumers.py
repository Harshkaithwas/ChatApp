import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatRoom
from accounts.models import *
from django.contrib.auth.decorators import login_required
import jwt
from django.contrib.auth import get_user_model
from jwt.exceptions import ExpiredSignatureError, DecodeError
from rest_framework_simplejwt.exceptions import TokenError
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
from django.db.models import Q



User = get_user_model()


User = get_user_model()

# users = Account.objects.get(id)

payload = {
    # 'user_id': users.id,
    # 'username': users.username
}

# Then, encode the JWT with the modified payload:
token = jwt.encode(payload, 'django-insecure-wq3ztblo3xffvkhz0q^ylvmd)$oig9i0vv*i-v8=$%h@p=s8gh', algorithm='HS256')
secret_key='django-insecure-wq3ztblo3xffvkhz0q^ylvmd)$oig9i0vv*i-v8=$%h@p=s8gh'

@database_sync_to_async
def verify_jwt_token(token, secret_key):

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = decoded_token['user_id']

        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get('query_string', b'').decode("utf-8")
        query_params = query_string.split("=")
        
        if len(query_params) == 2 and query_params[0] == 'access_token':
            access_token = query_params[1]
            secret_key = 'django-insecure-wq3ztblo3xffvkhz0q^ylvmd)$oig9i0vv*i-v8=$%h@p=s8gh'
            user = await verify_jwt_token(access_token, secret_key)
            
            if user is None:
                await self.close()
            else:
                self.room_name = self.scope['url_route']['kwargs']['room_name']
                self.room_group_name = f"chat_{self.room_name}"

                self.scope['user_id'] = user.id
                await self.accept()

        else:
            await self.close()


    # @database_sync_to_async
    async def get_user_by_id(self, user_id):
        try:
            return await database_sync_to_async(User.objects.get)(id=user_id)
        except User.DoesNotExist:
            return None






    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        user_id = self.scope.get('user_id')

        if user_id is not None:
            try:
                sender = await self.get_user_by_id(user_id)
                await self.save_message(sender, message)
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                # Broadcast the message to all participants including the sender
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.message',
                        'message': message,
                        'sender': sender.username,
                    }
                )
            except User.DoesNotExist:
                sender = "Anonymous"
        else:
            sender = "Anonymous"




    @database_sync_to_async
    def save_message(self, sender, message_text):
        try:
            chat_room = ChatRoom.objects.get(name=self.room_name)
            message = Message(sender=sender, content=message_text, room=chat_room)
            message.save()
        except ChatRoom.DoesNotExist:
            print(f"Chat room with name '{self.room_name}' does not exist.")

    



    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))