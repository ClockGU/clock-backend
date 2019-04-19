from freezegun import freeze_time
from datetime import datetime
from api.models import Report
import pytest
import time
from api.models import User

from project_celery.tasks import create_reports_monthly


class TestCeleryBeats:
    @pytest.mark.django_db
    @freeze_time("2019-02-1")
    def test_start_of_month_report_creation(
        self, user_object, contract_ending_in_february
    ):
        print(User.objects.filter(is_active=True, is_staff=False))

        create_reports_monthly.delay()
        time.sleep(20)
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
