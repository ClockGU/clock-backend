import pytest
from rest_framework import serializers
from api.serializers import ContractSerializer
import pprint
from pytz import datetime


class TestContractSerializerValidation:
    @pytest.mark.django_db
    def test_validate_correct_data(self, valid_contract_json):
        ContractSerializer(data=valid_contract_json).is_valid(raise_exception=True)

    @pytest.mark.django_db
    def test_start_date_causality_validation(
        self, end_date_before_start_date_contract_json
    ):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(data=end_date_before_start_date_contract_json).is_valid(
                raise_exception=True
            )

    @pytest.mark.django_db
    def test_start_date_day_validation(self, start_date_day_incorrect_contract_json):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(data=start_date_day_incorrect_contract_json).is_valid(
                raise_exception=True
            )

    @pytest.mark.django_db
    def test_end_date_day_validation(self, end_date_day_incorrect_contract_json):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(data=end_date_day_incorrect_contract_json).is_valid(
                raise_exception=True
            )

    @pytest.mark.django_db
    def test_negative_hours_validation(self, negative_hours_contract_json):
        with pytest.raises(serializers.ValidationError) as e_info:
            ContractSerializer(data=negative_hours_contract_json).is_valid(
                raise_exception=True
            )
