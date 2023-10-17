# chat/urls.py
from django.urls import path
from . import views
# from chat.consumers import ChatConsumer


urlpatterns = [
    # API endpoints
    path('online_users/', views.OnlineUserListView.as_view(), name='online-users'),
    path('start/', views.ChatRoomCreateView.as_view(), name='start-chat'),
]
