# -*- coding: utf-8 -*-


# from .models import ExecutedBackup
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from django.conf import settings
from django.core import management
import sys


# class BackupCronJob(CronJobBase):
#     RUN_EVERY_MINS = 60 * 24 * 7 # every week
#     RUN_EVERY_MINS = 1
#
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'backend.backup_cron_job'    # a unique code
#
#     def do(self):
#         if not ExecutedBackup.objects.filter(createdAt__gte=datetime.now()-timedelta(hours=1)).exists():
#             if "linux" in sys.platform:
#                 kwargs = {}
#                 if settings.ENVIRONMENT == "preproduction":
#                     kwargs.update({
#                         "settings": "backend.settings.preproduction"
#                     })
#                 elif settings.ENVIRONMENT == "production":
#                     kwargs.update({
#                         "settings": "backend.settings.production"
#                     })
#                 management.call_command('dbbackup', **kwargs)
#                 management.call_command('mediabackup', **kwargs)
#                 ExecutedBackup.objects.create(
#                     comment="Automatically backup of {}".format(datetime.now().strftime("%d-%b-%Y (%H:%M)"))
#                 )
