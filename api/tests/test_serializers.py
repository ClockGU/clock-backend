import pytest
from rest_framework import serializers
from freezegun import freeze_time

from api.serializers import (
    ContractSerializer,
    ShiftSerializer,
    ClockedInShiftSerializer,
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=end_date_before_start_date_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_start_date_day_validation(
        self, start_date_day_incorrect_contract_querydict, plain_request_object
    ):
        """
        The  ContractSerializer is tested whether it raises a Validation
        if the start_date day is not the 1. or 15. of a month.
        :param start_date_day_incorrect_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=start_date_day_incorrect_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_end_date_day_validation(
        self, end_date_day_incorrect_contract_querydict, plain_request_object
    ):
        """
        The  ContractSerializer is tested whether it raises a Validation
        if the start_date day is not the 14. or last day of a month.
        :param end_date_day_incorrect_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=end_date_day_incorrect_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_negative_hours_validation(
        self, negative_hours_contract_querydict, plain_request_object
    ):
        """
        The  ContractSerializer is tested whether it raises a Validation
        if the hours value is negative.
        :param negative_hours_contract_querydict:
        :param plain_request_object:
        :return:
        """
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=negative_hours_contract_querydict,
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=contract_ending_in_february_querydict,
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=stopped_before_started_querydict,
                context={"request": plain_request_object},
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=stopped_on_next_day_querydict,
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
        with pytest.raises(serializers.ValidationError) as e_info:
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
        with pytest.raises(serializers.ValidationError) as e_info:
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=contract_not_belonging_to_user_querydict,
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
        with pytest.raises(serializers.ValidationError) as e_info:
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=tags_not_string_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @freeze_time("2019-02-10 00:00:00+00:00")
    @pytest.mark.django_db
    def test_shift_in_past_as_planned_fails(
        self, shift_is_planned_but_started_in_past_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=shift_is_planned_but_started_in_past_json_querydict,
                context={"request": plain_request_object},
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
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=valid_shift_querydict, context={"request": plain_request_object}
            ).is_valid(raise_exception=True)

    @freeze_time("2019-01-01 00:00:00+00:00")
    @pytest.mark.django_db
    def test_shift_in_future_was_reviewed_fails(
        self, shift_starting_in_future_was_reviewed_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=shift_starting_in_future_was_reviewed_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)


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
        :return:
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
        :return:
        """
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=clockedinshift_invalid_contract_json,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)
