from freezegun import freeze_time
from datetime import datetime

import pytest
import time
from celery.contrib.testing.worker import start_worker
from api.models import User, Report
from project_celery.tasks import create_reports_monthly
from project_celery.celery import app


class TestCeleryBeats:
    @pytest.mark.django_db(transaction=True)
    @freeze_time("2019-02-1")
    def test_start_of_month_report_creation(
        self, celery_test_fixture, user_object, contract_ending_in_february
    ):

        create_reports_monthly.delay()
        time.sleep(1)
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
