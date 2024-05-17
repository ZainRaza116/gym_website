# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import FileUploading.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')
print("writing settings")
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        FileUploading.routing.websocket_urlpatterns
    ),
})
