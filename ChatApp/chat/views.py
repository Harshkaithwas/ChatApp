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
        current_user = self.request.user
        # Get the friends of the current user
        friends = current_user.friends.all()
        
        # Filter the friends who are also online
        online_friends = friends.filter(is_online=True)
        
        return online_friends






class ChatRoomCreateView(CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def generate_random_room_name(self, length=8):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def create(self, request, *args, **kwargs):
        creator = self.request.user
        participant_id = self.request.data.get('participant')

        if not participant_id:
            return Response(
                {'error': 'Participant ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Check if the participant is a friend and is online
            participant = Account.objects.get(id=participant_id, is_online=True, friends=creator)

            room_name = self.generate_random_room_name()

            chat_room = ChatRoom.objects.create(name=room_name)
            chat_room.participants.add(creator, participant)

            data = {
                'room_id': chat_room.id,
                'room_name': chat_room.name,
                'participants': [user.id for user in chat_room.participants.all()]
            }

            return Response(data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response(
                {'error': 'The specified participant is not your online friend.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error creating chat room: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


