# chat/urls.py
from django.urls import path
from .views import (
    group_chat,
    create_room,
    chat_room,
    user_login,
    user_logout,
    user_register,
    rename_room,
    delete_room
    )

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
    path('group-chat/', group_chat, name='group_chat'),
    path('create-room/', create_room, name='create_room'),
    path('chat-room/<int:room_id>/', chat_room, name='chat_room'),
    path('rename-room/<int:room_id>/', rename_room, name='rename_room'),
    path('delete-room/<int:room_id>/', delete_room, name='delete_room'),
    # Add other URL patterns as needed
]
