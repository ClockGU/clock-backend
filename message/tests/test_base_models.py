from django.db import models


class TestMessageModelExists:
    """
    Test whether an object Message can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from message.models import Message

        assert issubclass(Message, models.Model)


class TestMessageModelFields:
    """
    Test suite with basic field tests whether all fields of the Message object exist and
    have the correct class instance and field attribute values.
    """

    def test_model_has_field_type(self, message_model_class):
        assert hasattr(message_model_class, "type")

    def test_model_has_field_de_title(self, message_model_class):
        assert hasattr(message_model_class, "de_title")

    def test_model_has_field_de_text(self, message_model_class):
        assert hasattr(message_model_class, "de_text")

    def test_model_has_field_en_title(self, message_model_class):
        assert hasattr(message_model_class, "en_title")

    def test_model_has_field_en_text(self, message_model_class):
        assert hasattr(message_model_class, "en_text")

    def test_model_has_field_valid_from(self, message_model_class):
        assert hasattr(message_model_class, "valid_from")

    def test_model_has_field_valid_to(self, message_model_class):
        assert hasattr(message_model_class, "valid_to")

    def test_field_type_type(self, message_model_class):
        assert isinstance(message_model_class._meta.get_field("type"), models.CharField)

    def test_field_type_de_title(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("de_title"), models.CharField
        )

    def test_field_type_de_text(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("de_text"), models.TextField
        )

    def test_field_type_en_title(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("en_title"), models.CharField
        )

    def test_field_type_en_text(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("en_text"), models.TextField
        )

    def test_field_type_valid_from(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("valid_from"), models.DateField
        )

    def test_field_type_valid_to(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("valid_to"), models.DateField
        )
