from __future__ import absolute_import

import random
import time

from django.contrib.auth.models import User
from project_celery.celery import app
from pytz import datetime
from dateutil.relativedelta import relativedelta

from api.models import User, Report


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
        for contract in user.contracts.all():
            if contract.start_date < date_now <= contract.end_date:
                last_report = Report.objects.get(
                    contract=contract, month_year=date_now - relativedelta(months=1)
                )
                carry_over_worktime = datetime.timedelta(0)

                if last_report:
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
