import json
from datetime import datetime

import pytest
import time
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from pytz import datetime, utc
from api.models import Contract, Shift, Report


class TestUpdateSignals:
    @pytest.mark.django_db
    def test_signal_updates_shifts_report(
        self, report_object, contract_object, user_object
    ):
        """
        Test if the Report Object belonging to a Shift gets updated on save.
        :param report_object:
        :param contract_object:
        :param user_object:
        :return:
        """
        # Creeate shift for 29.01. which is 2 hours long
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 14, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 16, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
        )

        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).hours == datetime.timedelta(hours=2)

    @pytest.mark.django_db
    def test_signal_updates_next_months_report(
        self, report_object, february_report_object, contract_object, user_object
    ):

        # Creeate shift for 29.01. which is 2 hours long
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 14, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 16, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 16, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
        )

        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 2, 1)
        ).hours == datetime.timedelta(hours=-18)
