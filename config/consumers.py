from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4000, reason="User is not authenticated or token is missing")
            return 
        self.room_group_name = f'ReportsSocket_{self.scope["user"].id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        await self.send(text_data=json.dumps({"message": "WebSocket connected!"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received: {text_data}")
        await self.send(text_data=json.dumps({"response": "Message received!"}))

    async def report_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({"message": message}))