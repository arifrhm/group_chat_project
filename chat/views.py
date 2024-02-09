# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from .forms import RoomCreationForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm


@login_required
def group_chat(request):
    rooms = Room.objects.all()
    return render(request, 'chat/group_chat.html', {'rooms': rooms})


@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            Room.objects.create(name=room_name)
            return redirect('group_chat')
    else:
        form = RoomCreationForm()

    return render(request, 'chat/create_room.html', {'form': form})


@login_required
def chat_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    messages = Message.objects.filter(room=room)

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data['content']
            sender = request.user
            Message.objects.create(content=content, room=room, sender=sender)
            return redirect('chat_room', room_id=room_id)
    else:
        message_form = MessageForm()

    return render(request, 'chat/chat_room.html',
                  {'room': room, 'messages': messages,
                   'message_form': message_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('group_chat')
            else:
                # Handle invalid login
                pass
    else:
        form = LoginForm()

    return render(request, 'chat/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('group_chat')
    else:
        form = RegistrationForm()

    return render(request, 'chat/register.html', {'form': form})
