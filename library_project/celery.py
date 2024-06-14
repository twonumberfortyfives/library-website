from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_project.settings")

app = Celery("library_project")  # Replace 'your_project' with your project's name.

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
