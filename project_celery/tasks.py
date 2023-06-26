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

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from pytz import datetime

from api.models import Report, User
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


@app.task(bind=True, default_retry_delay=10)
def create_reports_monthly(self):
    """
    This is a Periodical Task which creates a Report object for every active users
    currently running contracts on the first of the month.
    An active Contract is the current month is between it's start- and end_date.
    :param self:
    :return:
    """
    date_now = datetime.datetime.now().date()
    for user in User.objects.filter(is_active=True, is_staff=False):
        for contract in user.contracts.filter(
            start_date__lt=date_now, end_date__gte=date_now
        ):
            last_report = Report.objects.get(
                contract=contract, month_year=date_now - relativedelta(months=1)
            )
            carry_over_worktime = last_report.worktime - datetime.timedelta(
                minutes=contract.minutes
            )

            Report.objects.create(
                month_year=date_now,
                worktime=carry_over_worktime,
                contract=contract,
                user=user,
                created_by=user,
                modified_by=user,
            )
