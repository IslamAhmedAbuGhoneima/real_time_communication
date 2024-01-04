from channels.generic.websocket import AsyncWebsocketConsumer
from .templatetags.chatextra import initials
from django.utils.timesince import timesince
from chat_app.models import Room, Message
from account.models import User
from asgiref.sync import sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Scope in consumer like request in views
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Join room group
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Receive message from webSocket (front end)
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent', '')

        if type == "message":
            new_message = await self.create_message(name, message, agent)
            # Send message to group / room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "name": name,
                    "agent": agent,
                    'initials': initials(name),
                    'created_at': timesince(new_message.created_at)
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket (front end)
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_room(self):
        try:
            self.room = Room.objects.get(uuid=self.room_name)
        except:
            self.room = ''

    @sync_to_async
    def create_message(self, send_by, message, agent):
        message = Message.objects.create(
            body=message,
            send_by=send_by,
        )
        if agent:
            message.created_by = User.objects.get(id=agent)
            message.save()
        self.room.messages.add(message)
        return message
