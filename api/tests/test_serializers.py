import datetime

import pytest
from freezegun import freeze_time
from rest_framework import exceptions, serializers

from api.models import Report, Shift
from api.serializers import (
    ClockedInShiftSerializer,
    ContractSerializer,
    ReportSerializer,
    ShiftSerializer,
)


class TestContractSerializerValidation:
    """
    This Testsuit summerizes the Validation and Representation of the ContractSerializer.
    """

    @pytest.mark.freeze_time("2019-01-10")
    @pytest.mark.django_db
    def test_validate_correct_data(
        self, valid_contract_querydict, plain_request_object
    ):
        """
        The ContractSerializer is tested if a valid JSON passes validation.
        :param valid_contract_querydict:
        :param plain_request_object:
        :return:
        """
        ContractSerializer(
            data=valid_contract_querydict, context={"request": plain_request_object}
        ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_start_date_causality_validation(
        self, end_date_before_start_date_contract_querydict, plain_request_object
    ):
        """
        The ContractSerializer is tested whether it raises a ValidationError
        if the start and end dates are causally correct.
        :param end_date_before_start_date_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                data=end_date_before_start_date_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    # TODO: Add test which explicitly verifies that contract with 1. or 16. as start_date is allowed.
    @pytest.mark.django_db
    def test_start_date_day_validation(
        self, start_date_day_incorrect_contract_querydict, plain_request_object
    ):
        """
        The  ContractSerializer is tested whether it raises a Validation
        if the start_date day is not the 1. or 16. of a month.
        :param start_date_day_incorrect_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                data=start_date_day_incorrect_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    # TODO: Add test which explicitly verifies that contract with 15. or end of month as end_date is allowed.
    @pytest.mark.django_db
    def test_end_date_day_validation(
        self, end_date_day_incorrect_contract_querydict, plain_request_object
    ):
        """
        The  ContractSerializer is tested whether it raises a Validation
        if the start_date day is not the 15. or last day of a month.
        :param end_date_day_incorrect_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                data=end_date_day_incorrect_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_negative_minutes_validation(
        self, negative_minutes_contract_querydict, plain_request_object
    ):
        """
        The  ContractSerializer is tested whether it raises a Validation
        if the minutes value is negative.
        :param negative_minutes_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                data=negative_minutes_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.freeze_time("2019-03-01")
    @pytest.mark.django_db
    def test_contract_ended_in_past_validation(
        self, plain_request_object, contract_ending_in_february_querydict
    ):
        """

        :param plain_request_object:
        :param contract_ending_in_february_json:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                data=contract_ending_in_february_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.freeze_time("2019-02-01")
    @pytest.mark.django_db
    def test_start_date_update_invalid_if_shifts_exist_before(
        self,
        shifts_before_new_start_date_contract,
        contract_ending_in_february,
        start_date_after_months_with_shifts_contract_querydict,
        plain_request_object,
    ):
        """
        Test if it is allowed to change the start_date to a later month even though there exist
        shifts previous to the new_start_date
        :param shifts_before_new_start_date_contract:
        :param contract_ending_in_february:
        :param start_date_after_months_with_shifts_contract_querydict:
        :param plain_request_object:
        :return:
        """

        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                instance=contract_ending_in_february,
                data=start_date_after_months_with_shifts_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.freeze_time("2019-01-30")
    @pytest.mark.django_db
    def test_end_date_update_invalid_if_shifts_exist_after(
        self,
        shifts_after_new_end_date_contract,
        contract_ending_in_february,
        end_date_before_months_with_shifts_contract_querydict,
        plain_request_object,
    ):
        """
        Test if it is allowed to change the end_date to a earlier month even though there exist
        shifts afterwards to the new_end_date.
        :param shifts_after_new_end_date_contract:
        :param contract_ending_in_february:
        :param end_date_before_months_with_shifts_contract_querydict:
        :param plain_request_object:
        :return:
        """

        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                instance=contract_ending_in_february,
                data=end_date_before_months_with_shifts_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.freeze_time("2019-01-01")
    @pytest.mark.django_db
    def test_start_carry_over_non_zerofuture_contract(
        self,
        non_zero_initial_carryover_minutes_for_future_contract_querydict,
        plain_request_object,
    ):
        """
        Test if is allowed to set start_carry_over to a non-zero timedelta for contracts
        starting in the future.
        :param non_zero_initial_carryover_minutes_for_future_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                data=non_zero_initial_carryover_minutes_for_future_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.freeze_time("2019-3-1")
    @pytest.mark.django_db
    def test_update_initial_carryover_minutes_updates_reports(
        self,
        contract_ending_in_april,
        shift_contract_ending_in_april,
        plain_request_object,
    ):
        """
        Test wether the serializers update method also updates the Reports when we change the initial_carryover_minutes.
        :param contract_ending_in_april:
        :param shift_contract_ending_in_april:
        :return:
        """
        assert Report.objects.get(
            contract=contract_ending_in_april, month_year=datetime.date(2019, 3, 1)
        ).worktime == datetime.timedelta(hours=-30)

        seri = ContractSerializer(
            instance=contract_ending_in_april,
            data={"initial_carryover_minutes": 600},
            partial=True,
            context={"request": plain_request_object},
        )
        seri.is_valid(raise_exception=True)
        seri.save()

        assert Report.objects.get(
            contract=contract_ending_in_april, month_year=datetime.date(2019, 3, 1)
        ).worktime == datetime.timedelta(hours=-25)

    @pytest.mark.freeze_time("2019-3-1")
    @pytest.mark.django_db
    def test_update_start_date_recreates_reports(
        self,
        contract_ending_in_april,
        shift_contract_ending_in_april,
        plain_request_object,
    ):
        """
        Test wether the serializers update method deletes existing reports and recreates them when
        the start_date is updated.
        :param contract_ending_in_april:
        :param shift_contract_ending_in_april:
        :return:
        """

        assert Report.objects.filter(contract=contract_ending_in_april).count() == 3
        old_report_pk = Report.objects.filter(contract=contract_ending_in_april)[0].pk
        seri = ContractSerializer(
            instance=contract_ending_in_april,
            data={"start_date": datetime.date(2019, 2, 1)},
            partial=True,
            context={"request": plain_request_object},
        )
        seri.is_valid(raise_exception=True)
        seri.save()

        assert Report.objects.filter(contract=contract_ending_in_april).count() == 2
        assert not Report.objects.filter(pk=old_report_pk).exists()
        assert Report.objects.get(
            contract=contract_ending_in_april, month_year=datetime.date(2019, 2, 1)
        ).worktime == datetime.timedelta(hours=5)
        # The shift_contract_ending_in_april has a 5 hours duration
        assert Report.objects.get(
            contract=contract_ending_in_april, month_year=datetime.date(2019, 3, 1)
        ).worktime == datetime.timedelta(hours=-10)

    @pytest.mark.freeze_time("2019-3-1")
    @pytest.mark.django_db
    def test_update_carryover_and_start_date_correct_evaluated(
        self,
        user_object,
        contract_ending_in_april,
        shift_contract_ending_in_april,
        plain_request_object,
    ):
        """
        By the tests 'test_update_carryover_target_date_recreates_reports' and
        'test_update_initial_carryover_minutes_updates_reports' we allready checked that PATCH'ing
        (parital updates) works. In order to not bother checking the Reports etc. for PUT'ing
        we just test the logic which determines whether or not either carryover_target_date and/or
        initial_carryover_minutes change (see update method of ContractSerializer).
        :param contract_ending_in_april:
        :param shift_contract_ending_in_april:
        :param plain_request_object:
        :return:
        """
        data = {
            "name": "Test Contract1",
            "minutes": 1200,
            "start_date": datetime.date(2019, 2, 1),
            "end_date": datetime.date(2019, 4, 30),
            "user": str(user_object.id),
            "created_by": str(user_object.id),
            "modified_by": str(user_object.id),
            "created_at": contract_ending_in_april.created_at,
            "modified_at": contract_ending_in_april.modified_at,
            "initial_carryover_minutes": 600,
        }
        seri = ContractSerializer(
            instance=contract_ending_in_april,
            data=data,
            context={"request": plain_request_object},
        )
        seri.is_valid()
        validated_data = seri.validated_data
        carryover_target_date_changed = (
            validated_data.get("start_date")
            != contract_ending_in_april.start_date
        )
        initial_carryover_minutes_changed = (
            validated_data.get("initial_carryover_minutes")
            != contract_ending_in_april.initial_carryover_minutes
        )
        assert carryover_target_date_changed
        assert initial_carryover_minutes_changed

    @pytest.mark.freeze_time("2019-1-20")
    @pytest.mark.django_db
    def test_update_contract_end_date(
        self,
        contract_end_date_7_months_apart_json,
        plain_request_object,
        contract_object,
    ):
        with pytest.raises(serializers.ValidationError):
            ContractSerializer(
                instance=contract_object,
                data=contract_end_date_7_months_apart_json,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)


class TestShiftSerializerValidation:
    """
    This Testsuit summerizes the Validation and Representation of the ShiftSerializer.
    """

    @pytest.mark.django_db
    def test_validate_correct_data(self, valid_shift_querydict, plain_request_object):
        """
        The ShiftSerializer is tested if a valid JSON passes validation.
        :param valid_shift_querydict:
        :param plain_request_object:
        :return:
        """
        ShiftSerializer(
            data=valid_shift_querydict, context={"request": plain_request_object}
        ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_shift_not_createable_if_allready_exported_exist(
        self,
        valid_shift_querydict,
        plain_request_object,
        test_shift_creation_if_allready_exported,
    ):
        """
        Test that we can not create a Shift if allready exported Shifts exist for this month.
        :param valid_shift_querydict:
        :param plain_request_object:
        :param test_shift_creation_if_allready_exported:
        :return:
        """
        with pytest.raises(exceptions.PermissionDenied):
            ShiftSerializer(
                data=valid_shift_querydict, context={"request": plain_request_object}
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_stopped_on_next_day_validation(
        self, stopped_on_next_day_querydict, plain_request_object
    ):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the shift ends on a different day.
        :param stopped_on_next_day_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=stopped_on_next_day_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_stopped_before_started_validation(
        self, stopped_before_started_querydict, plain_request_object
    ):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the started and ended datetimes are causally incorrect.
        :param stopped_before_started_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=stopped_before_started_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_shift_started_before_contract_validation(
        self, shift_starts_before_contract_querydict, plain_request_object
    ):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the shift starts before the contract started.
        :param shift_starts_before_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_starts_before_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_shift_starts_ends_after_contract_validation(
        self, shift_starts_ends_after_contract_json_querydict, plain_request_object
    ):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the shift ends after the contract ends.
        :param shift_starts_ends_after_contract_json_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_starts_ends_after_contract_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_contract_not_belonging_to_user_validation(
        self, contract_not_belonging_to_user_querydict, plain_request_object
    ):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the provided contract does not belong to the provided user.
        :param contract_not_belonging_to_user_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=contract_not_belonging_to_user_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @freeze_time("2019-02-10 00:00:00+00:00")
    @pytest.mark.django_db
    def test_shift_in_past_as_planned_fails(
        self, shift_is_planned_but_started_in_past_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_is_planned_but_started_in_past_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @freeze_time("2019-01-01 00:00:00+00:00")
    @pytest.mark.django_db
    def test_shift_in_future_was_reviewed_fails(
        self, shift_starting_in_future_was_reviewed_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_starting_in_future_was_reviewed_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_reviewed_shift_on_sunday_not_allowed(
        self, shift_on_a_sunday_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_on_a_sunday_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @freeze_time("2019-01-01 00:00:00+00:00")
    @pytest.mark.django_db
    def test_shift_in_future_was_reviewed_fails(
        self, shift_starting_in_future_was_reviewed_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_starting_in_future_was_reviewed_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_reviewed_shift_on_sunday_not_allowed(
        self, shift_on_a_sunday_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=shift_on_a_sunday_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_reviewed_shift_on_holiday_typ_normal_not_allowed(
        self, normal_shift_on_a_holiday_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=normal_shift_on_a_holiday_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_reviewed_vacation_shift_day_exclusive(
        self, shift_object, vacation_shift_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=vacation_shift_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_reviewed_sick_shift_day_exclusive(
        self, shift_object, sick_shift_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=sick_shift_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_maximum_shift_length_ten_hour_fortyfive_minutes(
        self, ten_hour_fortyfive_minutes_shift_json_querydict, plain_request_object
    ):
        ShiftSerializer(
            data=ten_hour_fortyfive_minutes_shift_json_querydict,
            context={"request": plain_request_object},
        ).is_valid(raise_exception=False)

    @pytest.mark.django_db
    def test_eleven_hour_shift_not_allowed(
        self, eleven_hour_shift_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=eleven_hour_shift_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_creating_shift_in_not_owned_contract_not_allowed(
        self, valid_shift_different_contract_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=valid_shift_different_contract_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_type_validation(self, wrong_type_querydict, plain_request_object):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the provided shift type is incorrect.
        :param wrong_type_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=wrong_type_querydict, context={"request": plain_request_object}
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_tags_validation(self, tags_not_string_querydict, plain_request_object):
        """
        The  ShiftSerializer is tested whether it raises a Validation
        if the tags are incorrect.
        :param tags_not_string_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=tags_not_string_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2019-01-30")
    def test_report_update_called_on_update(
        self, plain_request_object, test_contract_change
    ):
        """
        Test if we change the contract of a shift wether the reports of both contracts are updated.

        We start with fresh 00:00 Reports
        :param test_contract_change:
        :return:
        """

        shift = Shift.objects.get(contract=test_contract_change[0])
        ShiftSerializer().update(shift, {"contract": test_contract_change[1]})

        assert Report.objects.get(
            contract=test_contract_change[0], month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(0)
        assert Report.objects.get(
            contract=test_contract_change[1], month_year=datetime.date(2019, 1, 1)
        ).worktime == datetime.timedelta(hours=2)


class TestClockedInShiftSerializer:
    """
    This Testsuit summerizes the Validation and Representation of the ClockedInShiftSerializer.
    """

    @pytest.mark.django_db
    def test_validate_correct_data(
        self, valid_clockedinshift_querydict, plain_request_object
    ):
        """
        The ClockedInShiftSerializer is tested if a valid JSON passes validation.
        :param valid_clockedinshift_querydict:
        :param plain_request_object:
        """
        ClockedInShiftSerializer(
            data=valid_clockedinshift_querydict,
            context={"request": plain_request_object},
        ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_contract_not_belonging_to_user_validation(
        self, clockedinshift_invalid_contract_json, plain_request_object
    ):
        """
        The  ClockedInShiftSerializer is tested whether it raises a Validation
        if the provided contract does not belong to the provided user.
        :param clockedinshift_invalid_contract_json:
        :param plain_request_object:
        """
        with pytest.raises(serializers.ValidationError):
            ShiftSerializer(
                data=clockedinshift_invalid_contract_json,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_invalid_clocking_on_day_with_vacation_shift(
        self, valid_vacation_shift, valid_clockedinshift_querydict, plain_request_object
    ):
        """
        The  ClockedInShiftSerializer is tested whether it raises a Validation
        Error if there is already a vacation shift on this day.
        :param valid_vacation_shift:
        :param valid_clockedinshift_querydict:
        :param plain_request_object:
        """
        with pytest.raises(serializers.ValidationError):
            ClockedInShiftSerializer(
                data=valid_clockedinshift_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_invalid_clocking_on_sunday(
        self, valid_clockedinshift_sunday_querydict, plain_request_object
    ):
        """
        The  ClockedInShiftSerializer is tested whether it raises a Validation
        Error if the clocked Shift is on a sunday.
        :param valid_clockedinshift_sunday_querydict:
        :param plain_request_object:
        """
        with pytest.raises(serializers.ValidationError):
            ClockedInShiftSerializer(
                data=valid_clockedinshift_sunday_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_invalid_clocking_on_holiday(
        self, valid_clockedinshift_holiday_querydict, plain_request_object
    ):
        """
        The  ClockedInShiftSerializer is tested whether it raises a Validation
        Error if the clocked Shift is on a holiday.
        :param valid_clockedinshift_holiday_querydict:
        :param plain_request_object:
        """
        with pytest.raises(serializers.ValidationError):
            ClockedInShiftSerializer(
                data=valid_clockedinshift_holiday_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)


class TestReportSerializer:
    @pytest.mark.django_db
    @pytest.mark.freeze_time("2020-02-01")
    def test_carry_over_next_month(self, contract_start_mid_january):
        """
        Testing that the carryover for the next month is only half the debit worktime for a full
        month.
        :param contract_start_mid_january:
        :return:
        """
        rep = Report.objects.get(
            contract=contract_start_mid_january,
            month_year=contract_start_mid_january.start_date.replace(day=1),
        )
        assert ReportSerializer(rep).data["carryover"] == "-10:19"

    @pytest.mark.django_db
    @pytest.mark.freeze_time("2020-02-01")
    def test_carry_over_last_month(self, contract_start_mid_january):
        """
        Testing that the carryover for of the last month, is half the actual debit_worktime if the contract
        started in the middle of the last month.
        :param contract_start_mid_january:
        :return:
        """
        rep = Report.objects.get(
            contract=contract_start_mid_january,
            month_year=contract_start_mid_january.end_date.replace(day=1),
        )
        assert ReportSerializer(rep).data["carryover_previous_month"] == "-10:19"
