from rest_framework import serializers
from calendar import monthrange
from api.models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        extra_kwargs = {
            # Will be set automatically by the Model
            "created_at": {"required": False},
            # Will be set automatically by the Model
            "modified_at": {"required": False},
            "created_by": {"write_only": True},
            "modified_by": {"write_only": True},
            "user": {"write_only": True},
        }

    def validate(self, attrs):
        """
        Object-level validation.
        Validate that the start_date is smaller than the end_date.
        :param attrs:
        :return:
        """

        if attrs.get("start_date") > attrs.get("end_date"):
            raise serializers.ValidationError(
                "Der Beginn eines Vertrages muss vor dessen Ende liegen."
            )

        return attrs

    def validate_start_date(self, start_date):
        """
        Check that the day of the start_date is the 1st or 15th day of the month.
        :param start_date:
        :return: hours
        """
        if start_date.day not in (1, 15):
            raise serializers.ValidationError(
                "Ein Vertrag darf nur am 1. oder 15. eines Monats beginnen."
            )

        return start_date

    def validate_end_date(self, end_date):
        """
        Check that the contract ends either on the 14. or last day of a month.
        :param end_date:
        :return:
        """
        if end_date.day not in (14, monthrange(end_date.year, end_date.month)[1]):
            raise serializers.ValidationError(
                "Ein Vertrag darf nur am 14. oder letzten Tag eines Monats enden."
            )

        return end_date

    def validate_hours(self, hours):
        """
        Check that the provided value for hours is greater than zero.
        :param hours:
        :return: hours
        """
        if hours <= 0:
            raise serializers.ValidationError(
                "Die Anzahl der Stunden muss größer 0 sein."
            )

        return hours
