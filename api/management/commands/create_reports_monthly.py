from __future__ import absolute_import

from django.contrib.auth.models import User

from api.models import Report
from api.utilities import update_reports
from project_celery.celery import app


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
            Report.objects.get_or_create(
                month_year=date_now,
                contract=contract,
                user=user,
                defaults={
                    "worktime": datetime.timedelta(minutes=0),
                    "vacation_time": datetime.timedelta(minutes=0),
                    "created_by": user,
                    "modified_by": user,
                },
            )
            update_reports(contract, date_now)
