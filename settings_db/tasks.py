from backend.celery import app
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.decorators import task
from datetime import timedelta
from backend.utils import send_email
from django.core import management
from django.conf import settings
@app.task
def test___task():
    print('test email task')
    send_email("Test celery", "Celery work perfectly", settings.EMAIL_HOST_USER, "kechkarayoub@gmail.com")
    print('........................')


# @app.task
# def backup_function():
#     kwargs = {}
#     if settings.ENVIRONMENT == "preproduction":
#         kwargs.update({
#             "settings": "backend.settings.preproduction"
#         })
#     elif settings.ENVIRONMENT == "production":
#         kwargs.update({
#             "settings": "backend.settings.production"
#         })
#     send_email("Begin", "settings: {}".format(kwargs["settings"]), settings.EMAIL_HOST_USER, "kechkarayoub@gmail.com")
#     management.call_command('dbbackup', **kwargs)
#     send_email("End Begin", "dbbackup is done now mediabackup", settings.EMAIL_HOST_USER, "kechkarayoub@gmail.com")
#     management.call_command('mediabackup', **kwargs)
#     send_email("End", "all is done", settings.EMAIL_HOST_USER, "kechkarayoub@gmail.com")
