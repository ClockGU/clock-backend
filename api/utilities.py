from api.models import Report, Contract
from django.db.models.signals import post_save
from pytz import datetime

# Receiver used for the main API


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
