from django.contrib import admin
from chat.models import *

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'content', 'timestamp')
    list_filter = ('room', 'sender', 'timestamp')
    search_fields = ('sender__username', 'content')
