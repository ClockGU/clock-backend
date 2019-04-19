from __future__ import absolute_import

import random
import time

from django.contrib.auth.models import User

from project_celery.celery import app
from pytz import datetime

from api.models import User, Report

#         crontab(0, 0, day_of_month="1")

# Example Tasks

# Task which creates 5 User DB-Entries
@app.task(bind=True, default_retry_delay=10)
def async_5_user_creation(self):
    for _ in range(5):
        print("This Task starts.")
        i = random.randint(0, 1000)
        User.objects.create(username="Tim{}".format(i))
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
    with open("check_if_run.txt", "w") as file:
        file.write("Was fired\n")
        date_now = datetime.datetime.now().date()
        for user in User.objects.filter(is_active=True, is_staff=False):
            file.write("Found users.\n")
            for contract in user.contracts.all():
                file.write("User has contract.\n")
                if contract.start_date < date_now <= contract.end_date:
                    Report.objects.create(
                        month_year=date_now,
                        hours=datetime.timedelta(0),
                        contract=contract,
                        user=user,
                        created_by=user,
                        modified_by=user,
                    )
                    file.write(
                        "created new report. at : {} \n".format(datetime.datetime.now())
                    )
