# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sugarcare.settings')

# Lazily import the routing inside a function
def get_application():
    from channels.routing import ProtocolTypeRouter, URLRouter
    from room.routing import websocket_urlpatterns

    return ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    })

application = get_application()
