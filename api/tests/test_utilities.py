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
        self,
        report_object,
        february_report_object,
        contract_ending_in_february,
        user_object,
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
            contract=contract_ending_in_february,
        )

        assert Report.objects.get(
            contract=contract_ending_in_february, month_year=datetime.date(2019, 2, 1)
        ).hours == datetime.timedelta(hours=-18)

    @pytest.mark.django_db
    def test_signal_updates_with_prev_month_carry_over(
        self,
        january_report_object,
        february_report_object,
        contract_ending_in_february,
        user_object,
    ):
        february_report_object.hours = datetime.timedelta(hours=2)
        february_report_object.save()
        shift = Shift.objects.create(
            started=datetime.datetime(2019, 2, 11, 14, tzinfo=utc),
            stopped=datetime.datetime(2019, 2, 11, 16, tzinfo=utc),
            created_at=datetime.datetime(2019, 2, 11, 16, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 2, 11, 16, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_ending_in_february,
        )
        # reassure that only 2 hours get added
        assert Report.objects.get(
            contract=contract_ending_in_february, month_year=datetime.date(2019, 2, 1)
        ).hours == datetime.timedelta(hours=4)
        shift.stopped = datetime.datetime(2019, 2, 11, 18, tzinfo=utc)
        shift.save(update_fields=["stopped"])

        assert Report.objects.get(
            contract=contract_ending_in_february, month_year=datetime.date(2019, 2, 1)
        ).hours == datetime.timedelta(hours=6)

    @pytest.mark.django_db
    def test_signal_only_updates_reviewed_shifts(
        self, report_object, contract_object, user_object
    ):
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
            was_reviewed=False,
        )
        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).hours == datetime.timedelta(0)
