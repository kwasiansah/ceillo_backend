"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from .settings.base import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.base')

application = get_wsgi_application()

application = WhiteNoise(application, root=MEDIA_ROOT)
application.add_files(root=MEDIA_ROOT, prefix=MEDIA_URL)
application.add_files(root=STATIC_ROOT, prefix=STATIC_URL)