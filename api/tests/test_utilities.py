from datetime import datetime

import pytest
from freezegun import freeze_time
from pytz import utc
import datetime
from api.models import Contract, Report, Shift
from api.utilities import relativedelta_to_string


def test_relativedelta_to_string_positive_delta(positive_relativedelta_object):
    result_string = relativedelta_to_string(positive_relativedelta_object)
    assert result_string == "148:23"


def test_relativedelta_to_string_negative_delta(negative_relativedelta_object):
    result_string = relativedelta_to_string(negative_relativedelta_object)
    assert result_string == "-148:23"


class ContractAutomaticReportCreation:
    """
    Test the create_report_after_contract_save recieverfunction invoked on Contract.save() method.

    1) Test that a Report exists for all months in the case start_date < carryover_target_date < today < end_date
      1.1) Test that the first Report in case 1) has the initial_carryover_minutes as worktime.
      1.2) Test that all other Reports in case 1.1) have worktime == timedelta(0)
    2) Test that only one Report exists if today < start_date == carryover_target_date.

    """

    @freeze_time("2020-04-10")
    @pytest.mark.django_db
    def test_all_reports_exist(self, user_object):
        """
        Test case 1).
        :param user_object:
        :return:
        """

        _contract = Contract.objects.create(
            user=user_object,
            name="Report Creation Test Contract",
            minutes=1200,
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2020, 7, 31),
            carryover_target_date=datetime.date(2020, 1, 1),
            initial_carryover_minutes=0,
            created_by=user_object,
            modified_by=user_object,
        )
        assert len(Report.objects.filter(contract=_contract)) == 4

    @freeze_time("2020-04-10")
    @pytest.mark.django_db
    def test_first_contract_correct_worktime(self, user_object):
        """
        Test case 1.1).
        :param user_object:
        :return:
        """
        _contract = Contract.objects.create(
            user=user_object,
            name="Report Creation Test Contract",
            minutes=1200,
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2020, 7, 31),
            carryover_target_date=datetime.date(2020, 2, 1),
            initial_carryover_minutes=300,
            created_by=user_object,
            modified_by=user_object,
        )
        assert Report.objects.get(
            contract=_contract, month_year=datetime.date(2020, 2, 1)
        ).worktime == datetime.timedelta(hours=5)

    @freeze_time("2020-04-10")
    @pytest.mark.django_db
    def test_rest_of_reports_zero_worktime(self, user_object):
        """
        Test case 1.2)
        :param user_object:
        :return:
        """
        _contract = Contract.objects.create(
            user=user_object,
            name="Report Creation Test Contract",
            minutes=1200,
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2020, 7, 31),
            carryover_target_date=datetime.date(2020, 2, 1),
            initial_carryover_minutes=300,
            created_by=user_object,
            modified_by=user_object,
        )

        reports = Report.objects.filter(contract=_contract).exclude(
            month_year=datetime.date(2020, 2, 1)
        )
        assert all([r.worktime == datetime.timedelta() for r in reports])

    @freeze_time("2020-04-10")
    @pytest.mark.django_db
    def test_reports_exists_for_future_contract(self, user_object):
        """
        Test case 2)
        :param user_object:
        :return:
        """
        _contract = Contract.objects.create(
            user=user_object,
            name="Report Creation Test Contract",
            minutes=1200,
            start_date=datetime.date(2020, 5, 1),
            end_date=datetime.date(2020, 7, 31),
            carryover_target_date=datetime.date(2020, 5, 1),
            initial_carryover_minutes=300,
            created_by=user_object,
            modified_by=user_object,
        )

        reports = Report.objects.filter(contract=_contract)
        assert reports.__len__() == 1
        assert reports.first().month_year == datetime.date(2020, 5, 1)


class TestUpdateSignals:
    @freeze_time("2019-02-15")
    @pytest.mark.django_db
    def test_signal_updates_with_prev_month_carry_over(
        self, report_update_user, report_update_contract
    ):
        """
        Test that on an update the Report Update signal takes the previous months minutes - Contract.minutes as carry over.
        :param report_update_user:
        :param report_update_contract:
        :param report_update_february_report:
        :return:
        """
        shift = Shift.objects.create(
            started=datetime.datetime(2019, 2, 11, 14, tzinfo=utc),
            stopped=datetime.datetime(2019, 2, 11, 16, tzinfo=utc),
            created_at=datetime.datetime(2019, 2, 11, 16, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 2, 11, 16, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=report_update_user,
            created_by=report_update_user,
            modified_by=report_update_user,
            contract=report_update_contract,
        )

        shift.stopped = datetime.datetime(2019, 2, 11, 18, tzinfo=utc)
        shift.save()

        assert Report.objects.get(
            contract=report_update_contract, month_year=datetime.date(2019, 2, 1)
        ).worktime == datetime.timedelta(minutes=-960)

    @freeze_time("2019-02-05")
    @pytest.mark.django_db
    def test_signal_uses_initial_carryover_minutes(self, user_object):

        _contract = Contract.objects.create(
            user=user_object,
            name="Report Creation Test Contract",
            minutes=1200,
            start_date=datetime.date(2019, 1, 1),
            end_date=datetime.date(2019, 7, 31),
            carryover_target_date=datetime.date(2019, 2, 1),
            initial_carryover_minutes=300,
            created_by=user_object,
            modified_by=user_object,
        )
        Shift.objects.create(
            started=datetime.datetime(2019, 2, 11, 14, tzinfo=utc),
            stopped=datetime.datetime(2019, 2, 11, 16, tzinfo=utc),
            created_at=datetime.datetime(2019, 2, 11, 16, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 2, 11, 16, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=_contract,
        )
        assert Report.objects.get(
            contract=_contract, month_year=datetime.date(2019, 2, 1)
        ).worktime == datetime.timedelta(minutes=420)

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
        # Create shift for 29.01. which is 120 minutes long
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
        ).worktime == datetime.timedelta(minutes=120)

    @freeze_time("2020-02-15")
    @pytest.mark.django_db
    def test_signal_updates_next_months_report(
        self, contract_ending_in_february, user_object
    ):

        # Create shift for 29.01. which is 120 minutes long
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
        ).worktime == datetime.timedelta(minutes=-1080)

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
        ).worktime == datetime.timedelta(0)

    @pytest.mark.django_db
    def test_signal_updates_report_after_shift_deletion(
        self, contract_object, user_object, shift_object
    ):
        """
        Test that the Report get's updated after a Shift was deleted.
        :param contract_object:
        :param user_object:
        :param shift_object:
        :return:
        """
        # Sanity check
        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(minutes=120)
        shift_object.delete()
        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(0)

    @pytest.mark.django_db
    # @pytest.mark.freeze_time("2019-02-15")
    def test_signal_updates_next_months_report_after_shift_deletion(
        self, contract_ending_in_february, shift_object_february_contract
    ):
        """
        Test that not only the Report in which the Shift takes place is updated
        but also the next months Report.
        :return:
        """

        assert Report.objects.get(
            contract=contract_ending_in_february, month_year=datetime.date(2019, 2, 1)
        ).worktime == datetime.timedelta(minutes=-1080)
        shift_object_february_contract.delete()
        assert Report.objects.get(
            contract=contract_ending_in_february, month_year=datetime.date(2019, 2, 1)
        ).worktime == datetime.timedelta(minutes=-1200)

    @pytest.mark.django_db
    def test_signal_subtracts_missing_45_min_breaktime(
            self, contract_object, user_object
    ):
        """
        Test that the Report update subtraqcts missing 45 min breaks for Shift durations above 9h.
        """
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 8, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 18, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
            was_reviewed=True,
        )
        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(seconds=9.25*3600)

    @pytest.mark.django_db
    def test_signal_subtracts_missing_30_min_breaktime(
            self, contract_object, user_object
    ):
        """
        Test that the Report update subtracts missing 30 min breaks for Shift durations above 6h and lower than 9h.
        """
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 8, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 15, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
            was_reviewed=True,
        )
        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(seconds=6.5*3600)

    @pytest.mark.django_db
    def test_signal_doesnt_subtract_missing_breaktime(
            self, contract_object, user_object
    ):
        """
        Test that the report update does not substract any breaktime if not needed.
        """
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 8, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 12, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
            was_reviewed=True,
        )
        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(seconds=4*3600)

    @pytest.mark.django_db
    def test_signal_subtract_missing_breaktime(
            self, contract_object, user_object
    ):
        """
        Test that the report update does substract missing breaktime.

        Shift 1: 8:00-12:00
        Shift 2: 12:15-18:00
        Worktime 9:45
        Breaktime: 00:15

        Missing Breaktiem : 00:30
        """
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 8, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 12, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
            was_reviewed=True,
        )

        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 12, 15, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 18, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 19, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_object,
            was_reviewed=True,
        )

        assert Report.objects.get(
            contract=contract_object, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(seconds=9.25*3600)

    @pytest.mark.django_db
    def test_max_carryover_200h(self, contract_210h_carryover, user_object):
        """
        Test if the report update uses at max 200h carryover of the previous month.
        Tested here with a Contract that has initial_carryover_minutes
        equivalent to 210h and creation of a 3h long shift.
        """
        Shift.objects.create(
            started=datetime.datetime(2019, 1, 29, 10, tzinfo=utc),
            stopped=datetime.datetime(2019, 1, 29, 13, tzinfo=utc),
            created_at=datetime.datetime(2019, 1, 29, 10, tzinfo=utc).isoformat(),
            modified_at=datetime.datetime(2019, 1, 29, 10, tzinfo=utc).isoformat(),
            type="st",
            note="smth",
            user=user_object,
            created_by=user_object,
            modified_by=user_object,
            contract=contract_210h_carryover,
            was_reviewed=True,
        )

        assert Report.objects.get(
            contract=contract_210h_carryover, month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(hours=203)


class TestContractSignals:
    @pytest.mark.django_db
    def test_update_last_used(self, user_object, contract_object, freezer):
        time_stamp = datetime.datetime(2019, 2, 15, 1, 0, 0)
        assert contract_object.last_used != time_stamp
        freezer.move_to(time_stamp)
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
        assert contract_object.last_used == time_stamp
