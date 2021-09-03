import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GenesisV2.settings')

app = Celery('GenesisV2')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': settings.CELERY_BROKER_URL,
    'default_timeout': 60 * 60
  }
}
