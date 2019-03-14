import pytest
from rest_framework import serializers
from api.serializers import ContractSerializer, ShiftSerializer
import pprint
from pytz import datetime


class TestContractSerializerValidation:
    @pytest.mark.django_db
    def test_validate_correct_data(
        self, valid_contract_querydict, plain_request_object
    ):
        ContractSerializer(
            data=valid_contract_querydict, context={"request": plain_request_object}
        ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_start_date_causality_validation(
        self, end_date_before_start_date_contract_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=end_date_before_start_date_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_start_date_day_validation(
        self, start_date_day_incorrect_contract_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=start_date_day_incorrect_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_end_date_day_validation(
        self, end_date_day_incorrect_contract_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=end_date_day_incorrect_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_negative_hours_validation(
        self, negative_hours_contract_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(
                data=negative_hours_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)


class TestShiftSerializerValidation:
    @pytest.mark.django_db
    def test_validate_correct_data(self, valid_shift_querydict, plain_request_object):
        ShiftSerializer(
            data=valid_shift_querydict, context={"request": plain_request_object}
        ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_stopped_before_started_validation(
        self, stopped_before_started_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=stopped_before_started_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_stopped_on_next_day_validation(
        self, stopped_on_next_day_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=stopped_on_next_day_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_shift_started_before_contract_validation(
        self, shift_starts_before_contract_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=shift_starts_before_contract_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_shift_starts_ends_after_contract_validation(
        self, shift_starts_ends_after_contract_json_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=shift_starts_ends_after_contract_json_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_contract_not_belonging_to_user_validation(
        self, contract_not_belonging_to_user_querydict, plain_request_object
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=contract_not_belonging_to_user_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_type_validation(self, wrong_type_querydict, plain_request_object):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=wrong_type_querydict, context={"request": plain_request_object}
            ).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_tags_validation(self, tags_not_string_querydict, plain_request_object):
        with pytest.raises(serializers.ValidationError) as e_info:
            ShiftSerializer(
                data=tags_not_string_querydict,
                context={"request": plain_request_object},
            ).is_valid(raise_exception=True)
