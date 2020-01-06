from rest_framework import serializers


class TestFeedbackSerializer:
    def test_serializer_has_user_name(self, feedback_serializer_field_dict):
        """
        Test Serializer has a user_name field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("user_name")

    def test_serializer_has_user_email(self, feedback_serializer_field_dict):
        """
        Test Serializer has a user_mail field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("user_email")

    def test_serializer_has_email_title(self, feedback_serializer_field_dict):
        """
        Test Serializer has a email_title field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("email_title")

    def test_serializer_has_email_content(self, feedback_serializer_field_dict):
        """
        Test Serializer has a email_content field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("email_content")

    def test_field_type_user_name(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("user_name"), serializers.CharField
        )

    def test_field_type_user_email(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("user_email"), serializers.EmailField
        )

    def test_field_type_email_title(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("email_title"), serializers.CharField
        )

    def test_field_type_email_content(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("email_content"), serializers.CharField
        )
