from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from datetime import timedelta, timezone
from accounts.models import Account  
import random
import string
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import permissions
from .models import ChatRoom
from accounts.models import Account
from .serializers import UserSerializer, ChatRoomSerializer



class OnlineUserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the currently authenticated user
        current_user = self.request.user

        # Filter the queryset to exclude the current user and include only online users
        queryset = Account.objects.filter(is_online=True).exclude(id=current_user.id)

        return queryset# You can adjust the permission as needed







class ChatRoomCreateView(CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def generate_random_room_name(self, length=8):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def create(self, request, *args, **kwargs):
        creator = self.request.user
        participant = self.request.data.get('participant')

        if not participant:
            return Response(
                {'error': 'Participant is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        room_name = self.generate_random_room_name()

        try:
            chat_room = ChatRoom.objects.create(name=room_name)
            chat_room.participants.add(creator, participant)

            data = {
                'room_id': chat_room.id,
                'room_name': chat_room.name,
                'participants': [user.id for user in chat_room.participants.all()]
            }

            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Error creating chat room: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    



