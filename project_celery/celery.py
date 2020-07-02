from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

app = Celery("clock-backend", broker=os.environ.get("RABBITMQ_URL"))

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_schedule = {
    # This Tasks gets scheduled for the first of each month.
    "create_reports_monthly": {
        "task": "project_celery.tasks.create_reports_monthly",
        "schedule": crontab(0, 0, day_of_month="1"),
    }
}
app.autodiscover_tasks()


# Needed for celery within tests.
# This was mentioned in : https://stackoverflow.com/questions/46530784/make-django-test-case-database-visible-to-celery
@app.task(name="celery.ping")
def ping():
    """Simple task that just returns 'pong'."""
    return "pong"
