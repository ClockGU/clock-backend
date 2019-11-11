from api.models import Report, Contract, Shift
from django.db.models.signals import post_save
from django.db.models import Sum, F, DurationField
from django.db.models.functions import Coalesce
from pytz import datetime
from dateutil.relativedelta import relativedelta

# Receiver used for the main API


def relativedelta_to_string(relative_time_delta):
    """
    Format a relativedelta object for string representation in the format +/- HH:MM.

    Example:

    relativedelta(days=-3, hours=-8) becomes -80:00.

    relativedelta(days=-1, hours=-8, minutes=-30) becomes -32:30.

    :param relative_time_delta:
    :return:
    """

    return "{hours:02g}:{minutes:02g}".format(
        hours=relative_time_delta.days * 24 + relative_time_delta.hours,
        minutes=abs(relative_time_delta.minutes),
    )


def timedelta_to_string(timedelta):
    """
    Format a timedelta object for string representation in the format HH:MM

    :param timedelta:
    :return:
    """
    hours, remainder = divmod(timedelta.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return "{hours:02g}:{minutes:02g}".format(hours=hours, minutes=minutes)


def create_report_after_contract_save(sender, instance, created, **kwargs):
    """
    Receiver Function to be called by the post_save signal of a Contract object.
    It creates a Report object for the month when the Contract starts.
    The User might create a Contract after it already started so we also create
    all Report objects for the months between the start month and 'now".

    State: 14. April 2019

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        _month_year = instance.start_date.replace(day=1)
        today = datetime.date.today()
        # Always create a Report for the month it start.
        # This concerns Contracts starting in the future.
        Report.objects.create(
            month_year=_month_year,
            hours=datetime.timedelta(0),
            contract=instance,
            user=instance.user,
            created_by=instance.user,
            modified_by=instance.user,
        )
        _month_year += relativedelta(months=1)
        # If today is inbetween start and end date create Reports for all months
        # between start and today.
        while _month_year <= today:
            Report.objects.create(
                month_year=_month_year,
                hours=datetime.timedelta(0),
                contract=instance,
                user=instance.user,
                created_by=instance.user,
                modified_by=instance.user,
            )
            _month_year += relativedelta(months=1)


post_save.connect(
    create_report_after_contract_save,
    sender=Contract,
    dispatch_uid="create_report_after_contract_save",
)


def update_report_after_shift_save(sender, instance, created, **kwargs):
    """
    After saving a Shift we need to update the corresponding Report to reflect the now
    possibly updated overall work time.

    While updating we skip the whole mechanism if a Shift is planned (was_reviewd=False).
    Furthermore we skip all planned Shifts inside the Update mechanism.

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # Only run the Report update mechanism if a Shift which is not planned (was_reviewd=True) is
    # saved. Planned Shifts are not considered while updating Reports.
    if not instance.was_reviewed:
        return None

    debit_worktime = datetime.timedelta(hours=instance.contract.hours)
    current_month_year = instance.started.date().replace(day=1)

    previous_report = Report.objects.filter(
        contract=instance.contract,
        month_year=current_month_year - relativedelta(months=1),
    )
    carry_over_hours = datetime.timedelta(0)
    if previous_report.exists():
        carry_over_hours = previous_report.first().hours - debit_worktime
    # Loop over all Reports starting from month in which the created/update shift
    # took place.
    for report in Report.objects.filter(
        contract=instance.contract, month_year__gte=current_month_year
    ):
        total_work_time = Shift.objects.filter(
            contract=report.contract,
            started__month=report.month_year.month,
            started__year=report.month_year.year,
            was_reviewed=True,
        ).aggregate(
            total_work_time=Coalesce(
                Sum(F("stopped") - F("started"), output_field=DurationField()),
                datetime.timedelta(0),
            )
        )[
            "total_work_time"
        ]
        report.hours = carry_over_hours + total_work_time
        report.save()
        carry_over_hours = report.hours - debit_worktime


post_save.connect(
    update_report_after_shift_save,
    sender=Shift,
    dispatch_uid="update_report_after_shift_save",
)
