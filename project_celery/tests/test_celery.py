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
import time
from datetime import datetime, timedelta

import django.db
import pytest

from api.models import Report
from project_celery.tasks import create_reports_monthly


class TestCeleryBeats:
    @pytest.mark.freeze_time("2019-01-31")
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_start_of_month_report_creation(
        self, celery_test_fixture, user_object, contract_ending_in_february, freezer
    ):
        """
        Test the periodical task which creates a Report for every user, and each of his contracts, at
        the first of each month.
        :param celery_test_fixture:
        :param user_object:
        :param contract_ending_in_february:
        :return:
        """

        freezer.move_to("2019-02-01")
        create_reports_monthly()
        time.sleep(10)
        _month_year = datetime.now().date()

        assert (
            Report.objects.filter(
                user=user_object, contract=contract_ending_in_february
            ).count()
            == 2
        )
        assert Report.objects.get(
            user=user_object,
            contract=contract_ending_in_february,
            month_year=_month_year,
        )

    @pytest.mark.freeze_time("2019-01-31")
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_start_of_month_report_creation_correct_minutes(
        self,
        celery_test_fixture_correct_minutes,
        user_object,
        contract_ending_in_february,
        freezer,
    ):
        """
        Test that the automatic Report creation correctly carries over the minutes of the last month.

        In the Report for January, in this case, has a value for minutes of timedelta(minutes=600).
        The contract specifies 1200 minutes as debit.
        The carry over should turn out to be timedelta(minutes=-600) for February.
        :param celery_test_fixture_correct_minutes:
        :param user_object:
        :param contract_ending_in_february:
        :return:
        """
        freezer.move_to("2019-02-01")
        create_reports_monthly()
        time.sleep(10)

        assert Report.objects.get(
            contract=contract_ending_in_february, month_year__month=2
        ).worktime == timedelta(minutes=0)
        assert Report.objects.get(
            contract=contract_ending_in_february, month_year__month=2
        ).carryover_previous_month == timedelta(minutes=-600)

    @pytest.mark.freeze_time("2019-12-01")
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_start_of_month_report_creation_year_change(
        self,
        celery_test_fixture_end_of_year_test,
        user_object,
        december_contract,
        freezer,
    ):
        """
        Test that the monthly Report creation also works correctly at the beginning of a new year (1. January).
        :param celery_test_fixture_correct_minutes:
        :param user_object:
        :param contract_ending_in_february:
        :return:
        """
        freezer.move_to("2020-01-01")
        create_reports_monthly()
        time.sleep(10)

        assert Report.objects.get(
            contract=december_contract, month_year=datetime(2020, 1, 1)
        ).worktime == timedelta(minutes=-0)
        assert Report.objects.get(
            contract=december_contract, month_year=datetime(2020, 1, 1)
        ).carryover_previous_month == timedelta(minutes=-1200)

    @pytest.mark.freeze_time("2019-12-01")
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_idempotency_of_report_creation(
            celery_test_fixture_end_of_year_test,
            user_object,
            december_contract,
            freezer
    ):
        """
        Tetst that the function is idempotent in case of databse hiccups or other unforseen disturbances.
        """
        freezer.move_to("2020-01-01")
        create_reports_monthly()
        time.sleep(10)
        try:
            create_reports_monthly()
        except django.db.IntegrityError:
            raise pytest.fail("DID RAISE IntegrityError")
