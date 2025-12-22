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
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
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


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        email,
        password,
        first_name="",
        last_name="",
        personal_number="",
        username="",
        **extra_fields,
    ):
        """
        Create and save a user with the given username, email, password, first_name, last_name and personal_number.
        """

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            personal_number=personal_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email="",
        first_name="",
        last_name="",
        personal_number="",
        password="",
        username="",
        **extra_fields,
    ):
        if not email:
            raise ValueError("The field 'email' is required.")
        if not first_name:
            raise ValueError("The field 'first_name' is required.")
        if not last_name:
            raise ValueError("The field 'last_name' is required.")
        if not password:
            raise ValueError("The field 'password' is required.")
        # We always set the provided username to the user's email
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            personal_number=personal_number,
            **extra_fields,
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    LANGUAGE_CHOICES = (("de", "Deutsch"), ("en", "English"))
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    username = models.CharField(max_length=151, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)  # Firstname is required
    last_name = models.CharField(max_length=100)  # Lastname is required
    personal_number = models.CharField(
        max_length=100, default="", null=True, blank=True
    )
    language = models.CharField(choices=LANGUAGE_CHOICES, default="de", max_length=2)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    dsgvo_accepted = models.BooleanField(default=False)
    onboarding_passed = models.BooleanField(default=False)
    marked_for_deletion = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    supervised_references = ArrayField(
        default=list, base_field=models.CharField(max_length=50, null=True), blank=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "personal_number"]

    objects = CustomUserManager()


class Contract(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        to=User, related_name="contracts", on_delete=models.CASCADE
    )
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
    created_by = models.ForeignKey(
        to=User, related_name="+", on_delete=models.CASCADE
    )  # No backwards relation to these Fields
    last_used = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        to=User, related_name="+", on_delete=models.CASCADE
    )  # No backwards relation to these Fields


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
    user = models.ForeignKey(to=User, related_name="shifts", on_delete=models.CASCADE)
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
    created_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)


class ClockedInShift(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.OneToOneField(
        to=User, related_name="clocked_in_shift", on_delete=models.CASCADE
    )
    started = models.DateTimeField()
    contract = models.OneToOneField(
        to=Contract, related_name="clocked_in_shift", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)


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
    user = models.ForeignKey(to=User, related_name="reports", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)

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
