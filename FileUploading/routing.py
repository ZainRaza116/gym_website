# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws2/', consumers.CameraConsumer.as_asgi()),
]
