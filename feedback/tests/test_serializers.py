from rest_framework import serializers


class TestFeedbackSerializer:
    def test_serializer_has_name(self, feedback_serializer_field_dict):
        """
        Test serializer has a name field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("name")

    def test_serializer_has_email(self, feedback_serializer_field_dict):
        """
        Test serializer has a mail field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("email")

    def test_serializer_has_title(self, feedback_serializer_field_dict):
        """
        Test serializer has a title field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("title")

    def test_serializer_has_message(self, feedback_serializer_field_dict):
        """
        Test serializer has a message field.
        :param feedback_serializer_field_dict:
        :return:
        """
        assert feedback_serializer_field_dict.get("message")

    def test_field_type_name(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("name"), serializers.CharField
        )

    def test_field_type_email(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("email"), serializers.EmailField
        )

    def test_field_type_title(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("title"), serializers.CharField
        )

    def test_field_type_message(self, feedback_serializer_field_dict):
        assert isinstance(
            feedback_serializer_field_dict.get("message"), serializers.CharField
        )
