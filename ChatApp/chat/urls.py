# chat/urls.py
from django.urls import path
from . import views
from .consumers import ChatConsumer
# from chat.views import FriendsRecommendationView

urlpatterns = [
    # API endpoints
    path('online_users/', views.OnlineUserListView.as_view(), name='online-users'),
    path('start/', views.ChatRoomCreateView.as_view(), name='start-chat'),
    # path('suggested_friends/<int:user_id>/', FriendsRecommendationView.as_view(), name='suggested_friends'),

    # WebSocket chat
    # path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi(), name='chat-room'),
]
