from datetime import datetime, timedelta

import pytest
import time
from api.models import Report
from project_celery.tasks import create_reports_monthly
from project_celery.celery import app


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
        ).worktime == timedelta(minutes=-600)

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
        print(datetime.now().date())
        create_reports_monthly()
        time.sleep(10)

        print([f.month_year for f in Report.objects.filter(contract=december_contract)])
        assert Report.objects.get(
            contract=december_contract, month_year=datetime(2020, 1, 1)
        ).worktime == timedelta(minutes=-1200)
