"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
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
