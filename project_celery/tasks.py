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

from __future__ import absolute_import

import random
import time

from django.contrib.auth.models import User
from pytz import datetime

from api.idm.deprovisioning import Deprovisioner
from api.models import Report, User
from api.utilities import update_reports
from project_celery.celery import app


# Task which creates 5 User DB-Entries
@app.task(bind=True, default_retry_delay=10)
def async_5_user_creation(self):
    for _ in range(5):
        print("This Task starts.")
        i = random.randint(0, 1000)
        User.objects.create(email="Tim{}.test@test.com".format(i))
        print("This Task ends.")


# Task which prints a Start Message, sleeps 20 sec, and prints End message
# Visualization that all workers are used.
@app.task(bind=True, default_retry_delay=10)
def twenty_second_task(self, i):
    print("This Task begins {}.".format(i))
    time.sleep(20)
    print("This Task ends.")


