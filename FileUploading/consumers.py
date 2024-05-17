# consumers.py
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class CameraConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        # Process received frame
        # You can save it to a file, perform analysis, etc.
        print('Received frame:', text_data)

    async def disconnect(self, close_code):
        pass  # Clean up if needed
