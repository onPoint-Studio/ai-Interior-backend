import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AI_Interior.settings')
app = Celery('AI_Interior')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
