# chat/urls.py
from django.urls import path
from .views import (group_chat,
                    create_room,
                    chat_room,
                    user_login,
                    user_logout,
                    user_register)

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('group-chat/', group_chat, name='group_chat'),
    path('create-room/', create_room, name='create_room'),
    path('chat-room/<int:room_id>/', chat_room, name='chat_room'),
    # Add other URL patterns as needed
]
