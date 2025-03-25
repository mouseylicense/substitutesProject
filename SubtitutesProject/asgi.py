"""
ASGI config for SubtitutesProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SubtitutesProject.settings')
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from LaptopLoaning.routing import websocket_urlpatterns
from SubtitutesProject import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SubtitutesProject.settings')

application = get_asgi_application()
if settings.LAPTOPS_ENABLED:
    application = ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
        }
    )
