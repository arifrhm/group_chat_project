import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from chat.models import Message, Room


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        if self.scope['user'].is_anonymous:
            # If user is not authenticated, close the WebSocket connection
            self.close()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json['message']
            sender_id = text_data_json['sender_id']
            room_id = text_data_json['room_id']
            print(room_id)
            # Get the sender user instance
            sender = User.objects.get(id=sender_id)

            # Get the room instance
            room = Room.objects.get(id=room_id)

            # Create and save the message
            message = Message(content=message_content,
                              room=room, sender=sender)
            message.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message_content
                }
            )
        except json.JSONDecodeError:
            print("Received data is not a valid JSON")
        except KeyError:
            print("Received data does not contain 'message'" +
                  "or 'sender_id' or 'room_id' key")
        except User.DoesNotExist:
            print("Sender does not exist")
        except Room.DoesNotExist:
            print("Room does not exist")

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
