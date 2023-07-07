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
from datetime import datetime
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from pytz import utc


class TestCreateReportsCommand:
    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-02")
    def test_no_report_created_if_report_exists(self, contract_object):
        """
        Test if the command skips the creation of a Report in the specified month if one already exists.
        It's tested here with a Contract that only last for one month and hence got the Report created on
        Contract creation.

        :param contract_object:
        :return:
        """
        out = StringIO()
        call_command("create_reports", "1", "2019", stdout=out)

        assert "0 Reports were created." in out.getvalue()

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-02")
    def test_created_report_successful(self, contract_ending_in_february, freezer):
        """
        Test that the command actually creates a Report.
        :param contract_ending_in_february:
        :param freezer:
        :return:
        """
        freezer.move_to("2019-02-02")
        out = StringIO()
        call_command("create_reports", "2", "2019", stdout=out)

        assert "1 Reports were created." in out.getvalue()

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-02")
    def test_created_report_fails_for_future_dates(self, contract_object):
        """
        Test that the command does not allow creation of reports in the future.
        :param contract_object:
        :return:
        """
        out = StringIO()
        with pytest.raises(CommandError):
            call_command("create_reports", "2", "2019", stdout=out)


class TestUpdateReportsCommand:
    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-04-01")
    def test_all_reports_updated(self, contract_ending_in_april, contract_model_class):
        """
        Test that the command updates all Reports of contracts for which
        start_date <= date(year, month, 1) <= end_date is True.
        :param contract_ending_in_april:
        :return:
        """
        out = StringIO()
        call_command("update_reports", "3", "2019", stdout=out)
        contract = contract_model_class.objects.get(pk=contract_ending_in_april.pk)
        now = datetime.now(tz=utc)

        assert all([rep.modified_at == now for rep in contract.reports.all()])
