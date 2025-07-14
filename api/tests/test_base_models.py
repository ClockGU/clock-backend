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
import uuid

import freezegun
import pytest
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class TestUserModelExists:
    def test_model_existence(self):
        """
        This Test tests if an Object User can be imported.
        :return:
        """
        from api.models import User

    def test_model_is_model(self):
        """
        Test if the User Object is a Django Model
        :return:
        """
        from api.models import User

        assert issubclass(User, models.Model)


class TestContractModelExists:
    def test_model_existence(self):
        """
        This Test tests if an Object Contract can be imported.
        :return:
        """
        from api.models import Contract

    def test_model_is_model(self):
        """
        Test if the Contract Object is a Django Model
        :return:
        """
        from api.models import Contract

        assert issubclass(Contract, models.Model)


class TestShiftModelExists:
    def test_model_existence(self):
        """
        This Test tests if an Object Shift can be imported.
        :return:
        """
        from api.models import Shift

    def test_model_is_model(self):
        """
        Test if the Shift Object is a Django Model
        :return:
        """
        from api.models import Shift

        assert issubclass(Shift, models.Model)


class TestClockedInShiftModelExists:
    def test_model_existence(self):
        """
        This Test test if an Object ClockedInShift can be imported.
        :return:
        """
        from api.models import ClockedInShift

    def test_model_is_model(self):
        """
        Test if the ClockedInShift Object is a Django Model.
        :return:
        """
        from api.models import ClockedInShift

        assert issubclass(ClockedInShift, models.Model)


class TestReportModelExists:
    def test_model_existence(self):
        """
        This Test tests if an Object Report can be imported.
        :return:
        """
        from api.models import Report

    def test_model_is_model(self):
        """
        Test if the Report Object is a Django Model
        :return:
        """
        from api.models import Report

        assert issubclass(Report, models.Model)


class TestUserFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id_field(self, user_model_class):
        assert hasattr(user_model_class, "id")

    def test_model_has_email_field(self, user_model_class):
        assert hasattr(user_model_class, "email")

    def test_model_has_first_name_field(self, user_model_class):
        assert hasattr(user_model_class, "first_name")

    def test_model_has_last_name_field(self, user_model_class):
        assert hasattr(user_model_class, "last_name")

    def test_model_has_personal_number_filed(self, user_model_class):
        assert hasattr(user_model_class, "personal_number")

    def test_model_has_created_at_field(self, user_model_class):
        assert hasattr(user_model_class, "date_joined")

    def test_model_has_modified_at_field(self, user_model_class):
        assert hasattr(user_model_class, "modified_at")

    def test_model_has_language_field(self, user_model_class):
        assert hasattr(user_model_class, "language")

    def test_model_has_dsgvo_accepted_field(self, user_model_class):
        assert hasattr(user_model_class, "dsgvo_accepted")

    def test_field_type_id(self, user_model_class):
        assert isinstance(user_model_class._meta.get_field("id"), models.UUIDField)

    def test_field_type_email(self, user_model_class):
        assert isinstance(user_model_class._meta.get_field("email"), models.EmailField)

    def test_field_type_first_name(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("first_name"), models.CharField
        )

    def test_field_type_last_name(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("last_name"), models.CharField
        )

    def test_field_type_personal_number(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("personal_number"), models.CharField
        )

    def test_field_type_created_at(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("date_joined"), models.DateTimeField
        )

    def test_field_type_modified_at(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("modified_at"), models.DateTimeField
        )

    def test_field_type_language(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("language"), models.CharField
        )

    def test_field_type_dsgvo_accepted(self, user_model_class):
        assert isinstance(
            user_model_class._meta.get_field("dsgvo_accepted"), models.BooleanField
        )

    def test_field_conf_id(self, user_model_class):
        field = user_model_class._meta.get_field("id")
        assert field.primary_key
        assert field.default == uuid.uuid4
        assert not field.editable


class TestContractFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id(self, contract_model_class):
        assert hasattr(contract_model_class, "id")

    def test_model_has_user(self, contract_model_class):
        assert hasattr(contract_model_class, "user")

    def test_model_has_name(self, contract_model_class):
        assert hasattr(contract_model_class, "name")

    def test_model_has_minutes(self, contract_model_class):
        assert hasattr(contract_model_class, "minutes")

    def test_model_has_start_date(self, contract_model_class):
        assert hasattr(contract_model_class, "start_date")

    def test_model_has_end_date(self, contract_model_class):
        assert hasattr(contract_model_class, "end_date")

    def test_model_has_created_at(self, contract_model_class):
        assert hasattr(contract_model_class, "created_at")

    def test_model_has_created_by(self, contract_model_class):
        assert hasattr(contract_model_class, "created_by")

    def test_model_has_modified_at(self, contract_model_class):
        assert hasattr(contract_model_class, "modified_at")

    def test_model_has_modified_by(self, contract_model_class):
        assert hasattr(contract_model_class, "modified_by")

    def test_model_has_initial_carry_over(self, contract_model_class):
        assert hasattr(contract_model_class, "initial_carryover_minutes")

    def test_model_has_initial_vacation_carryover(self, contract_model_class):
        assert hasattr(contract_model_class, "initial_vacation_carryover_minutes")

    def test_model_has_last_used(self, contract_model_class):
        assert hasattr(contract_model_class, "last_used")

    def test_model_has_color(self, contract_model_class):
        assert hasattr(contract_model_class, "color")

    def test_field_type_id(self, contract_model_class):
        assert isinstance(contract_model_class._meta.get_field("id"), models.UUIDField)

    def test_field_type_user(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("user"), models.ForeignKey
        )

    def test_field_type_name(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("name"), models.CharField
        )

    def test_field_type_minutes(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("minutes"), models.PositiveIntegerField
        )

    def test_field_type_start_date(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("start_date"), models.DateField
        )

    def test_field_type_end_date(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("end_date"), models.DateField
        )

    def test_field_type_created_at(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("created_at"), models.DateTimeField
        )

    def test_field_type_created_by(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("created_by"), models.ForeignKey
        )

    def test_field_type_last_used(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("last_used"), models.DateTimeField
        )

    def test_field_type_modified_at(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("modified_at"), models.DateTimeField
        )

    def test_field_type_modified_by(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("modified_by"), models.ForeignKey
        )

    def test_field_type_color(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("color"), models.CharField
        )

    def test_field_conf_id(self, contract_model_class):
        field = contract_model_class._meta.get_field("id")
        assert field.primary_key
        assert field.default == uuid.uuid4
        assert not field.editable

    def test_field_type_initial_carryover_minutes(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("initial_carryover_minutes"),
            models.IntegerField,
        )

    def test_field_type_initial_vacation_carryover(self, contract_model_class):
        assert isinstance(
            contract_model_class._meta.get_field("initial_vacation_carryover_minutes"),
            models.IntegerField,
        )


class TestShiftFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id(self, shift_model_class):
        assert hasattr(shift_model_class, "id")

    def test_model_has_user(self, shift_model_class):
        assert hasattr(shift_model_class, "user")

    def test_model_has_started(self, shift_model_class):
        assert hasattr(shift_model_class, "started")

    def test_model_has_stopped(self, shift_model_class):
        assert hasattr(shift_model_class, "stopped")

    def test_model_has_contract(self, shift_model_class):
        assert hasattr(shift_model_class, "contract")

    def test_model_has_type(self, shift_model_class):
        assert hasattr(shift_model_class, "type")

    def test_model_has_note(self, shift_model_class):
        assert hasattr(shift_model_class, "note")

    def test_model_has_tags(self, shift_model_class):
        assert hasattr(shift_model_class, "tags")

    def test_model_has_was_reviewed(self, shift_model_class):
        assert hasattr(shift_model_class, "locked")

    def test_model_has_locked(self, shift_model_class):
        assert hasattr(shift_model_class, "locked")

    def test_model_has_created_at(self, shift_model_class):
        assert hasattr(shift_model_class, "created_at")

    def test_model_has_created_by(self, shift_model_class):
        assert hasattr(shift_model_class, "created_by")

    def test_model_has_modified_at(self, shift_model_class):
        assert hasattr(shift_model_class, "modified_at")

    def test_model_has_modified_by(self, shift_model_class):
        assert hasattr(shift_model_class, "modified_by")

    def test_field_type_id(self, shift_model_class):
        assert isinstance(shift_model_class._meta.get_field("id"), models.UUIDField)

    def test_field_type_user(self, shift_model_class):
        assert isinstance(shift_model_class._meta.get_field("user"), models.ForeignKey)

    def test_field_type_started(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("started"), models.DateTimeField
        )

    def test_field_type_stopped(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("stopped"), models.DateTimeField
        )

    def test_field_type_contract(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("contract"), models.ForeignKey
        )

    def test_field_type_type(self, shift_model_class):
        assert isinstance(shift_model_class._meta.get_field("type"), models.CharField)

    def test_field_type_note(self, shift_model_class):
        assert isinstance(shift_model_class._meta.get_field("note"), models.TextField)

    def test_field_type_tags(self, shift_model_class):
        assert isinstance(shift_model_class._meta.get_field("tags"), TaggableManager)

    def test_field_type_was_reviewed(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("locked"), models.BooleanField
        )

    def test_field_typ_locked(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("locked"), models.BooleanField
        )

    def test_field_type_created_at(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("created_at"), models.DateTimeField
        )

    def test_field_type_created_by(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("created_by"), models.ForeignKey
        )

    def test_field_type_modified_at(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("modified_at"), models.DateTimeField
        )

    def test_field_type_modified_by(self, shift_model_class):
        assert isinstance(
            shift_model_class._meta.get_field("modified_by"), models.ForeignKey
        )

    def test_field_conf_id(self, shift_model_class):
        field = shift_model_class._meta.get_field("id")
        assert field.primary_key
        assert field.default == uuid.uuid4
        assert not field.editable

    def test_field_conf_user(self, shift_model_class, user_model_class):
        field = shift_model_class._meta.get_field("user")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_field_conf_contract(self, shift_model_class, contract_model_class):
        field = shift_model_class._meta.get_field("contract")
        assert issubclass(field.remote_field.model, contract_model_class)

    def test_field_conf_type(self, shift_model_class):
        choices = (
            ("st", _("Shift")),
            ("sk", _("Sick")),
            ("vn", _("Vacation")),
            ("bh", _("Bank Holiday")),
        )
        field = shift_model_class._meta.get_field("type")
        assert field.choices == choices

    def test_field_conf_was_reviewed(self, shift_model_class):
        field = shift_model_class._meta.get_field("was_reviewed")
        assert (
            field.default is True
        )  # if no default is provided django returns an object which would be allways True

    def test_field_conf_locked(self, shift_model_class):
        field = shift_model_class._meta.get_field("locked")
        assert not field.default

    def test_field_conf_created_at(self, shift_model_class):
        field = shift_model_class._meta.get_field("created_at")
        assert field.auto_now_add

    def test_field_conf_created_by(self, shift_model_class, user_model_class):
        field = shift_model_class._meta.get_field("created_by")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_field_conf_modified_at(self, shift_model_class):
        field = shift_model_class._meta.get_field("modified_at")
        assert field.auto_now

    def test_field_conf_modified_by(self, shift_model_class, user_model_class):
        field = shift_model_class._meta.get_field("modified_by")
        assert issubclass(field.remote_field.model, user_model_class)


class TestClockedInShiftFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "id")

    def test_model_has_user(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "user")

    def test_model_has_started(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "started")

    def test_model_has_contract(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "contract")

    def test_model_has_created_at(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "created_at")

    def test_model_has_created_by(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "created_by")

    def test_model_has_modified_at(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "modified_at")

    def test_model_has_modified_by(self, clockedinshift_model_class):
        assert hasattr(clockedinshift_model_class, "modified_by")

    def test_field_type_id(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("id"), models.UUIDField
        )

    def test_field_type_user(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("user"), models.ForeignKey
        )

    def test_field_type_started(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("started"), models.DateTimeField
        )

    def test_field_type_contract(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("contract"), models.ForeignKey
        )

    def test_field_type_created_at(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("created_at"),
            models.DateTimeField,
        )

    def test_field_type_created_by(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("created_by"), models.ForeignKey
        )

    def test_field_type_modified_at(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("modified_at"),
            models.DateTimeField,
        )

    def test_field_type_modified_by(self, clockedinshift_model_class):
        assert isinstance(
            clockedinshift_model_class._meta.get_field("modified_by"), models.ForeignKey
        )

    def test_field_conf_id(self, clockedinshift_model_class):
        field = clockedinshift_model_class._meta.get_field("id")
        assert field.primary_key
        assert field.default == uuid.uuid4
        assert not field.editable

    def test_field_conf_user(self, clockedinshift_model_class, user_model_class):
        field = clockedinshift_model_class._meta.get_field("user")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_field_conf_contract(
        self, clockedinshift_model_class, contract_model_class
    ):
        field = clockedinshift_model_class._meta.get_field("contract")
        assert issubclass(field.remote_field.model, contract_model_class)

    def test_field_conf_created_at(self, clockedinshift_model_class):
        field = clockedinshift_model_class._meta.get_field("created_at")
        assert field.auto_now_add

    def test_field_conf_created_by(self, clockedinshift_model_class, user_model_class):
        field = clockedinshift_model_class._meta.get_field("created_by")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_field_conf_modified_at(self, clockedinshift_model_class):
        field = clockedinshift_model_class._meta.get_field("modified_at")
        assert field.auto_now

    def test_field_conf_modified_by(self, clockedinshift_model_class, user_model_class):
        field = clockedinshift_model_class._meta.get_field("modified_by")
        assert issubclass(field.remote_field.model, user_model_class)


class TestReportFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id(self, report_model_class):
        assert hasattr(report_model_class, "id")

    def test_model_has_user(self, report_model_class):
        assert hasattr(report_model_class, "user")

    def test_model_has_month_year(self, report_model_class):
        assert hasattr(report_model_class, "month_year")

    def test_model_has_worktime(self, report_model_class):
        assert hasattr(report_model_class, "worktime")

    def test_model_has_vacation_time(self, report_model_class):
        assert hasattr(report_model_class, "vacation_time")

    def test_model_has_contract(self, report_model_class):
        assert hasattr(report_model_class, "contract")

    def test_model_has_created_at(self, report_model_class):
        assert hasattr(report_model_class, "created_at")

    def test_model_has_created_by(self, report_model_class):
        assert hasattr(report_model_class, "created_by")

    def test_model_has_modified_at(self, report_model_class):
        assert hasattr(report_model_class, "modified_at")

    def test_model_has_modified_by(self, report_model_class):
        assert hasattr(report_model_class, "modified_by")

    def test_field_type_id(self, report_model_class):
        assert isinstance(report_model_class._meta.get_field("id"), models.UUIDField)

    def test_field_type_user(self, report_model_class):
        assert isinstance(report_model_class._meta.get_field("user"), models.ForeignKey)

    def test_field_type_month_year(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("month_year"), models.DateField
        )

    def test_field_type_worktime(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("worktime"), models.DurationField
        )

    def test_field_type_vacation_time(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("vacation_time"), models.DurationField
        )

    def test_field_type_contract(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("contract"), models.ForeignKey
        )

    def test_field_type_created_at(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("created_at"), models.DateTimeField
        )

    def test_field_type_created_by(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("created_by"), models.ForeignKey
        )

    def test_field_type_modified_at(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("modified_at"), models.DateTimeField
        )

    def test_field_type_modified_by(self, report_model_class):
        assert isinstance(
            report_model_class._meta.get_field("modified_by"), models.ForeignKey
        )

    def test_field_conf_id(self, report_model_class):
        field = report_model_class._meta.get_field("id")
        assert field.primary_key
        assert field.default == uuid.uuid4
        assert not field.editable

    def test_field_conf_user(self, report_model_class, user_model_class):
        field = report_model_class._meta.get_field("user")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_field_conf_contract(self, report_model_class, contract_model_class):
        field = report_model_class._meta.get_field("contract")
        assert issubclass(field.remote_field.model, contract_model_class)

    def test_field_conf_created_at(self, report_model_class):
        field = report_model_class._meta.get_field("created_at")
        assert field.auto_now_add

    def test_field_conf_created_by(self, report_model_class, user_model_class):
        field = report_model_class._meta.get_field("created_by")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_field_conf_modified_at(self, report_model_class):
        field = report_model_class._meta.get_field("modified_at")
        assert field.auto_now

    def test_field_conf_modified_by(self, report_model_class, user_model_class):
        field = report_model_class._meta.get_field("modified_by")
        assert issubclass(field.remote_field.model, user_model_class)

    def test_ordering(self, report_model_class):
        assert report_model_class._meta.ordering == ["month_year"]

    def test_unique_together(self, report_model_class):
        assert report_model_class._meta.unique_together == (("month_year", "contract"),)


class TestReportProperties:
    def test_model_has_debit_worktime(self, report_model_class):
        assert hasattr(report_model_class, "debit_worktime")

    def test_model_has_debit_vacation_time(self, report_model_class):
        assert hasattr(report_model_class, "debit_vacation_time")

    def test_model_has_carryover(self, report_model_class):
        assert hasattr(report_model_class, "carryover")

    def test_model_has_vacation_carryover_next_month(self, report_model_class):
        assert hasattr(report_model_class, "vacation_carryover_next_month")

    def test_model_has_carryover_previous_month(self, report_model_class):
        assert hasattr(report_model_class, "carryover_previous_month")

    def test_model_has_vacation_carryover_previous_month(self, report_model_class):
        assert hasattr(report_model_class, "vacation_carryover_previous_month")

    @pytest.mark.django_db
    def test_field_type_debit_worktime(self, report_object):
        assert isinstance(report_object.debit_worktime, datetime.timedelta)

    @pytest.mark.django_db
    def test_field_type_debit_vacation_time(self, report_object):
        assert isinstance(report_object.debit_vacation_time, datetime.timedelta)

    @pytest.mark.django_db
    def test_field_type_carryover(self, report_object):
        assert isinstance(report_object.carryover, datetime.timedelta)

    @pytest.mark.django_db
    def test_field_type_vacation_carryover_next_month(self, report_object):
        assert isinstance(
            report_object.vacation_carryover_next_month, datetime.timedelta
        )

    @pytest.mark.django_db
    def test_field_type_carryover_previous_month(self, report_object):
        assert isinstance(report_object.carryover_previous_month, datetime.timedelta)

    @pytest.mark.django_db
    def test_field_type_vacation_carryover_previous_month(self, report_object):
        assert isinstance(
            report_object.vacation_carryover_previous_month, datetime.timedelta
        )

    @pytest.mark.django_db
    def test_field_type_debit_worktime_in_report_object(self, report_object):
        assert report_object.debit_worktime == datetime.timedelta(seconds=72000)

    @pytest.mark.django_db
    def test_field_type_debit_vacation_time_in_report_object(self, report_object):
        assert report_object.debit_vacation_time == datetime.timedelta(
            seconds=5519, microseconds=779209
        )

    @pytest.mark.django_db
    def test_field_type_carryover_in_report_object(self, report_object):
        assert report_object.carryover == datetime.timedelta(days=-1, seconds=14400)

    @pytest.mark.django_db
    def test_field_type_vacation_carryover_next_month_in_report_object(
        self, report_object
    ):
        assert report_object.vacation_carryover_next_month == datetime.timedelta(
            seconds=5519, microseconds=779209
        )

    @pytest.mark.django_db
    def test_field_type_carryover_previous_month_in_report_object(self, report_object):
        assert report_object.carryover_previous_month == datetime.timedelta(0)

    @pytest.mark.django_db
    def test_field_type_vacation_carryover_previous_month_in_report_object(
        self, report_object
    ):
        assert report_object.vacation_carryover_previous_month == datetime.timedelta(0)

    @pytest.mark.django_db
    @freezegun.freeze_time("2019-02-01")
    def test_carryover_account_with_initial_carryover(self, january_report_initial_carryover_account):
        """
        Test that the initial carryover of 41 hours is deducted 20 hours of
        debit worktime and a carryover of 21 hours is left.
        """
        assert january_report_initial_carryover_account.carryover == datetime.timedelta(
            minutes=1260
        )
        assert january_report_initial_carryover_account.debit_worktime == datetime.timedelta(
            minutes=1200
        )

    @pytest.mark.django_db
    @freezegun.freeze_time("2019-02-01")
    def test_carryover_account_correct_summation_of_shifts(self, report_initial_carryover_with_shifts_account):
        """
        Test that the initial carryover of 41 hours is deducted 20 hours of
        debit worktime and shifts of the month (2x 5h shift) are added to the carryover
        resulting in a carryover of 21 hours + 10 hours = 31 hours.
        """
        assert report_initial_carryover_with_shifts_account.carryover == datetime.timedelta(
            minutes=1860
        )
    @pytest.mark.django_db
    @freezegun.freeze_time("2019-02-01")
    def test_carryover_account_previous_month(self,february_report_initial_carryover_account):
        """
        Test that the carryover is correctly recognized by the report of the following month.
        """

        assert february_report_initial_carryover_account.carryover_previous_month == datetime.timedelta(minutes=1260)

    @pytest.mark.django_db
    @freezegun.freeze_time("2019-02-01")
    def test_carryover_account_with_new_overtime(self, report_carryover_with_additional_overtime):
        """
        Test that additional over time (5 hours) is correctly added to the account.
        41 h initial carryover
        25 h of shifts
        ----
        46 h carryover (2760 minutes)
        """
        assert report_carryover_with_additional_overtime.carryover == datetime.timedelta(minutes=2760)

    @pytest.mark.django_db
    @freezegun.freeze_time("2019-02-01")
    def test_carryover_account_with_too_much_new_overtime(self, report_carryover_with_too_much_additional_overtime):
        """
        Test that additional over time (5 hours) is correctly added to the account.
        41 h initial carryover
        35 h of shifts
        ----
        51 h carryover (3060 minutes)

        The carryover my only increase upto 50% of the debit worktime (10h in this case).
        """
        assert report_carryover_with_additional_overtime.carryover == datetime.timedelta(minutes=3060)