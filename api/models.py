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
import uuid
from calendar import monthrange
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from .validators import (
    FTE_WEEKYL_MINUTES,
    VALIDATOR_CLASS_NAMES,
    business_weeks,
    stud_emp_worktime_multiplicator,
    worktime_multiplicator,
)


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Contract(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    name = models.CharField(max_length=100)
    reference = models.UUIDField(default=uuid.uuid4)
    minutes = models.PositiveIntegerField()
    percent_fte = models.FloatField(
        null=True, blank=True, verbose_name="Prozent einer Vollzeitstelle"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    initial_carryover_minutes = models.IntegerField(default=0)
    initial_vacation_carryover_minutes = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default="#8ac5ff")
    worktime_model_name = models.CharField(
        max_length=200, choices=VALIDATOR_CLASS_NAMES, verbose_name="Validierungsklasse"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    last_used = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField


class Shift(models.Model):
    TYPE_CHOICES = (
        ("st", _("Shift")),
        ("sk", _("Sick")),
        ("vn", _("Vacation")),
        ("bh", _("Bank Holiday")),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    started = models.DateTimeField()
    stopped = models.DateTimeField()
    contract = models.ForeignKey(
        to=Contract, related_name="shifts", on_delete=models.CASCADE
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=2)
    note = models.TextField(blank=True)
    tags = TaggableManager(blank=True, through=UUIDTaggedItem)
    was_reviewed = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    modified_at = models.DateTimeField(auto_now=True)
    modified_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField


class ClockedInShift(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.UUIDField(unique=True)  # Changed from OneToOneField to UUIDField with unique=True
    started = models.DateTimeField()
    contract = models.OneToOneField(
        to=Contract, related_name="clocked_in_shift", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    modified_at = models.DateTimeField(auto_now=True)
    modified_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField


class Report(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    month_year = models.DateField()
    worktime = models.DurationField()
    vacation_time = models.DurationField(default=timedelta(0))
    contract = models.ForeignKey(
        to=Contract, related_name="reports", on_delete=models.CASCADE
    )
    user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField
    modified_at = models.DateTimeField(auto_now=True)
    modified_by_user_id = models.UUIDField()  # Changed from ForeignKey to UUIDField

    @property
    def debit_worktime(self):
        current_date = self.month_year
        month_end_day = monthrange(current_date.year, current_date.month)[1]
        start_date = self.contract.start_date
        end_date = self.contract.end_date

        if self.contract.worktime_model_name == "studEmp":
            return timedelta(
                minutes=self.contract.minutes
                * stud_emp_worktime_multiplicator(
                    current_date, start_date, end_date, month_end_day
                )
            )
        return timedelta(
            minutes=self.contract.percent_fte
            / 100
            * FTE_WEEKYL_MINUTES[self.contract.worktime_model_name]
            * worktime_multiplicator(current_date, start_date, end_date, month_end_day)
        )

    @property
    def debit_vacation_time(self):
        """
        Calculate the actual debit vacation time for a report.

        The actual debit vacation time can be lower than the provided value based on the contract due to:
        incomplete months (contract starts not at first, or end not on the last of a month.)

        Calculation description for vacation_seconds_per_month:
        ('Worktime per month' / 'avg weeks per month' / 'workdays per week') * 'general vacation days' / '12 months'

        Calculation for non student employees:
        Given an employee works on X days in a week he receives X/5 * 30 days of vacation.
        Since we are not saving the actual days of work, only the percent FTE, we can not compute this.
        Return 0

        """
        if self.contract.worktime_model_name == "studEmp":
            vacation_seconds_per_month = (
                ((self.contract.minutes * 60) / 4.348 / 5) * 20 / 12
            )

            return timedelta(
                seconds=(
                    self.debit_worktime.total_seconds()
                    / (self.contract.minutes * 60)
                    * vacation_seconds_per_month
                )
            )

        return timedelta()

    @property
    def carryover(self):
        carryover = self.worktime - self.debit_worktime + self.carryover_previous_month
        max_carryover_increase = self.debit_worktime / 2
        if carryover > self.carryover_previous_month + max_carryover_increase:
            return self.carryover_previous_month + max_carryover_increase
        return carryover

    @property
    def vacation_carryover_next_month(self):
        carryover_next_month = (
            self.debit_vacation_time + self.vacation_carryover_previous_month
        ) - self.vacation_time
        return carryover_next_month

    @cached_property
    def carryover_previous_month(self):
        try:
            last_mon_report_object = Report.objects.get(
                contract=self.contract,
                month_year=self.month_year - relativedelta(months=1),
            )

        except Report.DoesNotExist:
            return timedelta(minutes=self.contract.initial_carryover_minutes)

        return last_mon_report_object.carryover

    @property
    def vacation_carryover_previous_month(self):
        try:
            last_mon_report_object = Report.objects.get(
                contract=self.contract,
                month_year=self.month_year - relativedelta(months=1),
            )

        except Report.DoesNotExist:
            return timedelta(minutes=self.contract.initial_vacation_carryover_minutes)

        except Report.DoesNotExist:
            return timedelta(0)

        return last_mon_report_object.vacation_carryover_next_month

    class Meta:
        ordering = ["month_year"]
        unique_together = ["month_year", "contract"]
