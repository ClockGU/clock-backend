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

    @pytest.mark.freeze_time("2019-01-10")
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_skipping_contracts_already_having_a_report(
        self, user_object, contract_from_march_till_august, freezer
    ):
        """

        :param contract_from_march_till_august:
        :return:
        """
        assert (
            Report.objects.filter(
                user=user_object, contract=contract_from_march_till_august
            ).count()
            == 1
        )
        freezer.move_to("2019-03-01")
        create_reports_monthly()
        time.sleep(10)

        assert (
            Report.objects.filter(
                user=user_object,
                contract=contract_from_march_till_august,
                month_year__month=3,
            ).count()
            == 1
        )
