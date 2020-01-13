from freezegun import freeze_time
from datetime import datetime, timedelta

import pytest
import time
from api.models import User, Report, Contract
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
    def test_start_of_month_report_creation_correct_hours(
        self,
        celery_test_fixture_correct_hours,
        user_object,
        contract_ending_in_february,
        freezer,
    ):
        """
        Test that the automatic Report creation correctly carries over the hours of the last month.

        In the Report for January, in this case, has a value for hours of timedelta(hours=10).
        The contract specifies 20 hours as debit.
        The carry over should turn out to be timedelta(hours=-10) for February.
        :param celery_test_fixture_correct_hours:
        :param user_object:
        :param contract_ending_in_february:
        :return:
        """
        freezer.move_to("2019-02-01")
        create_reports_monthly()
        time.sleep(10)
        _month_year = datetime.now().date()

        assert Report.objects.get(
            contract=contract_ending_in_february, month_year__month=2
        ).hours == timedelta(hours=-10)

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
        Test that the monthly Report creation also works correctly at the Beginning of a new Year (1. January).
        :param celery_test_fixture_correct_hours:
        :param user_object:
        :param contract_ending_in_february:
        :return:
        """
        freezer.move_to("2020-01-01")
        create_reports_monthly()
        time.sleep(10)

        print(Report.objects.filter(contract=december_contract))
        assert Report.objects.get(
            contract=december_contract, month_year=datetime(2020, 2, 1)
        ).hours == timedelta(hours=-20)
