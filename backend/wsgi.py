"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
try:
    from .settings.special_settings import ENVIRONMENT
except:
    ENVIRONMENT = "production"
if ENVIRONMENT == "preproduction":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.preproduction')
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.production")

application = get_wsgi_application()
