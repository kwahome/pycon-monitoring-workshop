from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings
from structlog import get_logger

logger = get_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')

app = Celery('celery-{}'.format(settings.SERVICE))
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)