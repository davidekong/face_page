"""
ASGI config for face_page project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django import http

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_page.settings')

application = ProtocolTypeRouter({
    'http': AsgiHandler(), 
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
