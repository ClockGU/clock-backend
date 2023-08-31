from __future__ import absolute_import, unicode_literals

"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
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
    },
    "deprovision_users_monthly": {
        "task": "project_celery.tasks.deprovision_users_monthly",
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
