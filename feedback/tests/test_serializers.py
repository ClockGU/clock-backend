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
