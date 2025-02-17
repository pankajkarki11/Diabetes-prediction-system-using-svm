from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Room, Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handle WebSocket connection.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Fetch the room asynchronously
        try:
            self.room = await database_sync_to_async(Room.objects.get)(slug=self.room_name)
        except Room.DoesNotExist:
            await self.close()
            return

        # Add the user to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        """
        # Remove the user from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handle messages received via WebSocket.
        """
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '').strip()
            username = text_data_json.get('username')

            if not message or not username:
                return  # Ignore invalid or empty messages

            # Save the message to the database asynchronously
            await database_sync_to_async(self.save_message)(message, username)

            # Broadcast the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'message': message
                }
            )
        except json.JSONDecodeError:
            pass  # Handle invalid JSON gracefully

    async def chat_message(self, event):
        """
        Send a message to the WebSocket.
        """
        message = event['message']
        username = event['username']

        # Send the message as JSON to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message
        }))

    def save_message(self, message, username):
        """
        Save a chat message to the database.
        """
        try:
            user = User.objects.get(username=username)
            Message.objects.create(room=self.room, user=user, content=message)
        except (Room.DoesNotExist, User.DoesNotExist):
            pass 