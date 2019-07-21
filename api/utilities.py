from api.models import Report, Contract, Shift
from django.db.models.signals import post_save
from django.db.models import Sum, F, DurationField
from django.db.models.functions import Coalesce
from pytz import datetime
from dateutil.relativedelta import relativedelta


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


def update_report_after_shift_save(sender, instance, created, **kwargs):
    """
    After the saving a Shift we need to update the corresponding Report to reflect the now
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

    # Retrieve Report Object of interest
    report = Report.objects.get(
        contract=instance.contract,
        month_year__month=instance.started.month,
        month_year__year=instance.started.year,
    )
    # If a Shift is created we just need to add it's duration to the Report
    if created:
        update_value = instance.stopped - instance.started
        report.hours += update_value
        report.save()

        next_month_report = Report.objects.filter(
            month_year=report.month_year + relativedelta(months=1),
            contract=report.contract,
        ).first()
        if next_month_report:
            carry_over_hours = report.hours - datetime.timedelta(
                hours=report.contract.hours
            )
            update_report_with_carry_over(
                carry_over_hours=carry_over_hours, report_to_update=next_month_report
            )
    # If a Shift is updated we need to roll over all
    else:
        # Get the Report of the previous month
        # This one might not exist in the case that the Function is called in the First month of an active Contract
        last_months_report = Report.objects.filter(
            month_year=report.month_year - relativedelta(months=1),
            contract=instance.contract,
        ).first()
        carry_over_hours = datetime.timedelta(0)
        if last_months_report:
            carry_over_hours = last_months_report.hours - datetime.timedelta(
                hours=report.contract.hours
            )
        update_report_with_carry_over(carry_over_hours, report_to_update=report)


post_save.connect(
    update_report_after_shift_save,
    sender=Shift,
    dispatch_uid="create_report_after_contract_save",
)


def update_report_with_carry_over(carry_over_hours, report_to_update):
    """
    When updating a Report on Shift save we encounter the case that the Shift took place in the previous month.
    In this scenario the Report of the previous month gets updated which changes the already 'carried over' hours
    to this months Report. Hence the current Reports overall hours need to be recalculated.

    This function takes the Report which already has a following Report and updates the later.
    :param previeous_month_report:
    :param next_month_report:
    :return:
    """

    # reagregate the Total worktime of next_month_report
    total_work_time = Shift.objects.filter(
        contract=report_to_update.contract,
        started__month=report_to_update.month_year.month,
        started__year=report_to_update.month_year.year,
        was_reviewed=True,
    ).aggregate(
        total_work_time=Coalesce(
            Sum(F("stopped") - F("started"), output_field=DurationField()),
            datetime.timedelta(0),
        )
    )[
        "total_work_time"
    ]

    report_to_update.hours = carry_over_hours + total_work_time
    report_to_update.save()
    next_month_report = Report.objects.filter(
        month_year=report_to_update.month_year + relativedelta(months=1),
        contract=report_to_update.contract,
    ).first()

    if next_month_report:
        update_report_with_carry_over(report_to_update.hours, next_month_report)
