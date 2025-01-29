import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drScratch.settings')

app = Celery('drScratch')
app.config_from_object('django.conf:settings', namespace='CELERY')
worker_lost_timeout = 60

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')