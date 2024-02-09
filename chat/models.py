# chat/models.py
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)


class Message(models.Model):
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
