from api.models import Report, Contract
from django.db.models.signals import post_save
from pytz import datetime

# Receiver used for the main API


def relativedelta_to_string(relative_time_delta):
    """
    Format a relaativedelta object for string representation in the format +/- HH:MM:SS.

    Example:

    relativedelta(days=-3, hours=-8) becomes -80:00:00.

    relativedelta(days=-1, hours=-8, minutes=-30) becomes -32:30:00

    :param relative_time_delta:
    :return:
    """

    return "{hours:02g}:{minutes:02g}:{seconds:02g}".format(
        hours=relative_time_delta.days * 24 + relative_time_delta.hours,
        minutes=abs(relative_time_delta.minutes),
        seconds=abs(relative_time_delta.seconds),
    )


def create_report_after_contract_save(sender, instance, created, **kwargs):
    """
    Receiver Function to be called by the post_save signal of a Contract object.
    It creates a Report object for the month when the Contract starts.
    Hereby we neglect that a User could create a Contract which started in the past.

    State: 14. April 2019

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        _month_year = instance.start_date.replace(day=1)
        Report.objects.create(
            month_year=_month_year,
            hours=datetime.timedelta(0),
            contract=instance,
            user=instance.user,
            created_by=instance.user,
            modified_by=instance.user,
        )


post_save.connect(
    create_report_after_contract_save,
    sender=Contract,
    dispatch_uid="create_report_after_contract_save",
)
