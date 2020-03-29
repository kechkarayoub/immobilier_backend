from __future__ import absolute_import, unicode_literals
import django
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
try:
    from .settings.special_settings import ENVIRONMENT
except:
    ENVIRONMENT = "production"
if ENVIRONMENT == "production":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.production')
elif ENVIRONMENT == "preproduction":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.preproduction')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')
# django.setup()

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
