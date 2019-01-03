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
