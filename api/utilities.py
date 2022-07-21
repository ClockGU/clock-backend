from dateutil.relativedelta import relativedelta
from django.db.models import DurationField, F, Sum
from django.db.models.functions import Coalesce
from django.db.models.signals import post_delete, post_save
from pytz import datetime

from api.models import Contract, Report, Shift

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
    time_data = (
        relative_time_delta.days,
        relative_time_delta.hours,
        relative_time_delta.minutes,
    )
    format_string = "{hours:02g}:{minutes:02g}"
    if any(map(lambda x: x < 0, time_data)):
        format_string = "-{hours:02g}:{minutes:02g}"

    return format_string.format(
        hours=abs(relative_time_delta.days * 24 + relative_time_delta.hours),
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


# TODO: This function needs a different, more phony name.
def create_reports_for_contract(contract):
    """
    Function used to create all Reports from carryover_target_date to date.today().
    :param contract:
    :return:
    """
    _month_year = contract.carryover_target_date
    today = datetime.date.today()
    Report.objects.create(
        month_year=_month_year,
        worktime=datetime.timedelta(minutes=contract.initial_carryover_minutes),
        contract=contract,
        user=contract.user,
        created_by=contract.user,
        modified_by=contract.user,
    )
    _month_year += relativedelta(months=1)

    # Create Reports for all months between carryover_target_date and now
    while _month_year <= today:
        Report.objects.create(
            month_year=_month_year,
            worktime=datetime.timedelta(0),
            contract=contract,
            user=contract.user,
            created_by=contract.user,
            modified_by=contract.user,
        )
        _month_year += relativedelta(months=1)


def create_report_after_contract_creation(sender, instance, created, **kwargs):
    """
    Reciever function:
    Receiver Function to be called by the post_save signal of a Contract object.
    It creates a Report object for the month when the Contract starts.
    The User might create a Contract after it already started so we also create
    all Report objects for the months between the carryover_target_date month and 'now".

    State: 14. April 2019

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        create_reports_for_contract(contract=instance)


post_save.connect(
    create_report_after_contract_creation,
    sender=Contract,
    dispatch_uid="create_report_after_contract_save",
)


def update_reports(contract, month_year):
    """
    Update the Reports for the given contract starting with the given month/year.
    :param contract:
    :param month_year:
    :return:
    """
    # Loop over all Reports starting from month in which the created/update shift
    # took place.
    for report in Report.objects.filter(contract=contract, month_year__gte=month_year):
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
        carry_over_worktime = report.get_carry_over_last_month()
        report.worktime = carry_over_worktime + total_work_time
        report.save()
        # carry_over_worktime = report.worktime - report.debit_worktime


def update_report_after_shift_save(sender, instance, created=False, **kwargs):
    """
    Reciever function:
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

    current_month_year = instance.started.date().replace(day=1)
    update_reports(instance.contract, current_month_year)


post_save.connect(
    update_report_after_shift_save,
    sender=Shift,
    dispatch_uid="update_report_after_shift_save",
)
post_delete.connect(
    update_report_after_shift_save,
    sender=Shift,
    dispatch_uid="update_report_after_shift_delete",
)


def update_last_used_on_contract(sender, instance, created=False, **kwargs):
    """
    Reciever functions:
    After saving or deleting a shift set the `last_used` field of the corresponding
    contract.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    contract = instance.contract
    contract.last_used = datetime.datetime.now()
    contract.save()


post_save.connect(
    update_last_used_on_contract,
    sender=Shift,
    dispatch_uid="update_last_used_on_contract_save",
)
post_delete.connect(
    update_last_used_on_contract,
    sender=Shift,
    dispatch_uid="update_last_used_on_contract_delete",
)
