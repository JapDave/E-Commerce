import os
from EShop.settings import CELERY_RESULT_BACKEND, CELERY_TASK_TRACK_STARTED
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EShop.settings')

app = Celery('EShop',broker='redis://admin:Aditetech123$$@redis-13237.c264.ap-south-1-1.ec2.cloud.redislabs.com:13237/0',
CELERY_RESULT_BACKEND='redis://admin:Aditetech123$$@redis-13237.c264.ap-south-1-1.ec2.cloud.redislabs.com:13237/0',CELERY_TASK_TRACK_STARTED=True)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')