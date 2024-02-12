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
import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import (
    Case,
    DurationField,
    ExpressionWrapper,
    F,
    Max,
    Min,
    Sum,
    Value,
    When,
    Window,
)
from django.db.models.functions import Trunc
from django.db.models.signals import post_delete, post_save
from more_itertools import pairwise

from api.models import Contract, Report, Shift


def calculate_break(shifts_queryset, new_shift_started=None, new_shift_stopped=None):
    """
    Calculation of total breaks between shifts.

    @param started:
    @param stopped:
    @param shifts_queryset:
    @param new_shift:
    @return:
    """
    if not shifts_queryset.exists():
        return datetime.timedelta(seconds=0)
    shifts_queryset = shifts_queryset.order_by("started")

    total_break = datetime.timedelta()

    for shift, shift_next in pairwise(shifts_queryset):
        total_break += shift_next.started - shift.stopped

    if new_shift_started and new_shift_stopped:
        # new shift is after old shifts
        if new_shift_started >= shifts_queryset.last().stopped:
            return (new_shift_started - shifts_queryset.last().stopped) + total_break
        # new shift is before old shifts
        if new_shift_stopped <= shifts_queryset.first().started:
            return (shifts_queryset.first().started - new_shift_stopped) + total_break

        # new shift is in between old shifts
        return total_break - (new_shift_started - new_shift_stopped)
    return total_break


def calculate_worktime_breaktime(worktime, breaktime):
    """
    Calculate the work and break time of a day, depending on the minimal needed break.

    worktime > 9h --> needs minimum 45min break
    worktime > 6h and < 9h --> needs minimum 30min break

    @param worktime:
    @type worktime: datetime.timedelta
    @param breaktime:
    @type breaktime: datetime.timedelta
    @return:
    """
    if datetime.timedelta(hours=6) < worktime <= datetime.timedelta(hours=9):
        # Needed break >= 30min in total
        if breaktime < datetime.timedelta(minutes=30):
            worktime = worktime - datetime.timedelta(minutes=30) + breaktime
            breaktime = datetime.timedelta(minutes=30)
    elif worktime > datetime.timedelta(hours=9):
        # Needed break >= 45min in total
        if breaktime < datetime.timedelta(minutes=45):
            worktime = worktime - datetime.timedelta(minutes=45) + breaktime
            breaktime = datetime.timedelta(minutes=45)
    return worktime, breaktime


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
    format_string = "{hours:02g}:{minutes:02g}"
    seconds = timedelta.total_seconds()
    if seconds < 0:
        format_string = "-{hours:02g}:{minutes:02g}"
        seconds = -1*seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return format_string.format(hours=hours, minutes=minutes)


# TODO: This function needs a different, more phony name.
def create_reports_for_contract(contract):
    """
    Function used to create all Reports from contracts start_date to date.today().
    :param contract:
    :return:
    """
    _month_year = contract.start_date.replace(day=1)
    today = datetime.date.today()
    Report.objects.create(
        month_year=_month_year,
        worktime=datetime.timedelta(0),
        vacation_time=datetime.timedelta(0),
        contract=contract,
        user=contract.user,
        created_by=contract.user,
        modified_by=contract.user,
    )
    _month_year += relativedelta(months=1)

    # Create Reports for all months between start_date and now/end_date
    while _month_year <= today and _month_year <= contract.end_date:
        Report.objects.create(
            month_year=_month_year,
            worktime=datetime.timedelta(0),
            vacation_time=datetime.timedelta(0),
            contract=contract,
            user=contract.user,
            created_by=contract.user,
            modified_by=contract.user,
        )
        _month_year += relativedelta(months=1)
    update_reports(contract, contract.start_date)


def create_report_after_contract_creation(sender, instance, created, **kwargs):
    """
    Reciever function:
    Receiver Function to be called by the post_save signal of a Contract object.
    It creates a Report object for the month when the Contract starts.
    The User might create a Contract after it already started so we also create
    all Report objects for the months between the start_date month and 'now".

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
        shifts_this_day = Shift.objects.filter(
            contract=report.contract,
            started__month=report.month_year.month,
            started__year=report.month_year.year,
            was_reviewed=True,
        )
        data_per_day = shifts_this_day.annotate(
            day_worktime=ExpressionWrapper(
                Window(
                    expression=Sum(F("stopped") - F("started")),
                    partition_by=[Trunc("started", "day")],
                ),
                DurationField(),
            ),
            first_started=Window(
                expression=Min("started"), partition_by=[Trunc("started", "day")]
            ),
            last_stopped=Window(
                expression=Max("stopped"), partition_by=[Trunc("started", "day")]
            ),
        ).distinct("started__date")
        breaktime_data = data_per_day.annotate(
            breaktime=ExpressionWrapper(
                F("last_stopped") - F("first_started") - F("day_worktime"),
                DurationField(),
            ),
            missing_breaktime=Case(
                When(
                    day_worktime__gt=datetime.timedelta(hours=6),
                    day_worktime__lte=datetime.timedelta(hours=9),
                    breaktime__lt=datetime.timedelta(minutes=30),
                    then=datetime.timedelta(minutes=30) - F("breaktime"),
                ),
                When(
                    day_worktime__gt=datetime.timedelta(hours=9),
                    breaktime__lt=datetime.timedelta(minutes=45),
                    then=datetime.timedelta(minutes=45) - F("breaktime"),
                ),
                default=Value(datetime.timedelta(0)),
                output_field=DurationField(),
            ),
        )
        report.worktime = sum(
            map(
                lambda shift: shift.day_worktime - shift.missing_breaktime,
                breaktime_data,
            ),
            datetime.timedelta(0),
        )
        report.vacation_time = sum(
            map(
                lambda shift: shift.stopped - shift.started,
                shifts_this_day.filter(
                    type="vn",
                ),
            ),
            datetime.timedelta(0),
        )
        report.save()


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
