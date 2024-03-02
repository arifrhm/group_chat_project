# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from .forms import RoomCreationForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from .forms import StyledUserCreationForm, RoomRenameForm
from django.contrib import messages


@login_required
def group_chat(request):
    rooms = Room.objects.all()
    return render(request, 'group_chat.html', {'rooms': rooms})


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

    return render(request, 'create_room.html',
                  {'form': form})


@login_required
def rename_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = RoomRenameForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('group_chat')
    else:
        form = RoomRenameForm(instance=room)

    return render(request, 'rename_room.html',
                  {'form': form, 'room': room})


@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.delete()
        return redirect('group_chat')

    return render(request, 'delete_room.html', {'room': room})


@login_required
def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room=room)
    # chat_consumer_instance = ChatConsumer()
    # await chat_consumer_instance.connect()

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data['content']
            sender = request.user
            # await database_sync_to_async(Message.objects.create)(
            #     content=content, room=room, sender=sender)
            # await chat_consumer_instance.receive(sender.username, content)
            print(content)
            print(sender)
    else:
        message_form = MessageForm()

    return render(request, 'chat_room.html',
                  {'room': room, 'messages': messages,
                   'message_form': message_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('group_chat')  # Change to your desired URL
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid login details given")

    return render(request, 'login.html',
                  {'messages': messages.get_messages(request)})


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


def user_register(request):
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('group_chat')
    else:
        form = StyledUserCreationForm()

    return render(request, 'register.html', {'form': form})
