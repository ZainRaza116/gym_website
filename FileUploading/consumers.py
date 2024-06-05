import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import time

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connection established")
        self.last_frame_time = None

    async def disconnect(self, close_code):
        print("WebSocket connection closed")

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
