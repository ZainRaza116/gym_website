# routing.py
from django.urls import path
from FileUploading.consumers import VideoConsumer

websocket_urlpatterns = [
    path('ws/video/', VideoConsumer.as_asgi()),
]
