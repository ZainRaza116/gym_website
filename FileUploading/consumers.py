# views.py
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64

class CameraConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.last_frame_time = None  
        super().__init__()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        frame_data = text_data_json['frame']
        show_colored_overlay = text_data_json.get('show_colored_overlay', False)
        show_angles_on_overlay = text_data_json.get('show_angles_on_overlay', False)
        show_info_table = text_data_json.get('show_info_table', False)

        # Decode the base64 image
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Apply the image_set filter with toggle states
        processed_frame = self.image_set(frame, show_colored_overlay, show_angles_on_overlay, show_info_table)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        processed_frame_data = base64.b64encode(buffer).decode('utf-8')
        await self.send(text_data=json.dumps({
            'processed_frame': f'data:image/jpeg;base64,{processed_frame_data}'
        }))

    def image_set(self, img, show_colored_overlay, show_angles_on_overlay, show_info_table):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        equ = cv2.equalizeHist(gray) 
        blurred = cv2.GaussianBlur(src=equ, ksize=(3, 5), sigmaX=0.5) 
        edges = cv2.Canny(blurred, 70, 135)
        print(show_angles_on_overlay, show_colored_overlay, show_info_table)
        
        return edges
