import pytest
from django.db import models


class TestUserModelExists:
    def test_model_existence(self):
        """
        This Test tests if an Object User can be imported.
        :return:
        """

        from api.models import User

    def test_model_is_model(self):
        """
        Test if the User Object is a Django Model
        :return:
        """
        from api.models import User

        assert issubclass(User, models.Model)


class TestContractModelExists:
    def test_model_existence(self):
        """
        This Test tests if an Object User can be imported.
        :return:
        """

        from api.models import Contract

    def test_model_is_model(self):
        """
        Test if the User Object is a Django Model
        :return:
        """
        from api.models import Contract

        assert issubclass(Contract, models.Model)


class TestUserFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id_field(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "id")

    def test_model_has_email_field(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "email")

    def test_model_has_first_name_field(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "first_name")

    def test_model_has_last_name_field(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "last_name")

    def test_model_has_personal_number_filed(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "personal_number")

    def test_model_has_created_at_field(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "created_at")

    def test_model_has_modified_at_field(self, user_model_class_instace):
        assert hasattr(user_model_class_instace, "modified_at")

    def test_field_type_id(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("id"), models.UUIDField
        )

    def test_field_type_email(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("email"), models.EmailField
        )

    def test_field_type_first_name(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("first_name"), models.CharField
        )

    def test_field_type_last_name(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("last_name"), models.CharField
        )

    def test_field_type_personal_number(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("personal_number"),
            models.CharField,
        )

    def test_field_type_created_at(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("created_at"), models.DateTimeField
        )

    def test_field_type_modified_at(self, user_model_class_instace):
        assert isinstance(
            user_model_class_instace._meta.get_field("modified_at"),
            models.DateTimeField,
        )


class TestContractFields:
    """
    This Testsuit summerizes the basic field tests:
    1. Do all fields exist
    2. Do all fields have the correct format/class instance
    """

    def test_model_has_id(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "id")

    def test_model_has_user(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "user")

    def test_model_has_name(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "name")

    def test_model_has_hours(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "hours")

    def test_model_has_start_date(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "start_date")

    def test_model_has_end_date(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "end_date")

    def test_model_has_created_at(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "created_at")

    def test_model_has_created_by(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "created_by")

    def test_model_has_modified_at(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "modified_at")

    def test_model_has_modified_by(self, contract_model_class_instance):
        assert hasattr(contract_model_class_instance, "modified_by")

    def test_field_type_id(self, contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("id"), models.UUIDField)

    def test_field_type_user(self,contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("user"), models.ForeignKey)

    def test_field_type_name(self,contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("name"), models.CharField)
        
    def test_field_type_hours(self,contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("hours"), models.FloatField)
        
    def test_field_type_start_date(self,contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("start_date"), models.DateField)
        
    def test_field_type_end_date(self, contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("end_date"), models.DateField)

    def test_field_type_created_at(self, contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("created_at"), models.DateTimeField)
        
    def test_field_type_created_by(self, contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("created_by"), models.ForeignKey)

    def test_field_type_modified_at(self, contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("modified_at"), models.DateTimeField)

    def test_field_type_modified_by(self, contract_model_class_instance):
        assert isinstance(contract_model_class_instance._meta.get_field("modified_by"), models.ForeignKey)
