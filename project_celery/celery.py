from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

app = Celery("clock-backend", broker=os.environ.get("RABBITMQ_URL"))

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_schedule = {
    "create_reports_monthly": {
        "task": "project_celery.tasks.create_reports_monthly",
        "schedule": crontab(0, 0, day_of_month="1"),
    }
}
app.autodiscover_tasks()
