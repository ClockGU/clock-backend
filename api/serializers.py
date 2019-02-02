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
        Here we validate : start_date is, timewise, prior to end_date
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
        Furthermore we check that the day of the start_date is the first or 15th of the month.
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
        We check that the Contract ends either on the 14. or last day of a month.
        :param end_date:
        :return:
        """
        if end_date.day not in (14, monthrange(end_date.year, end_date.month)[1]):
            raise serializers.ValidationError(
                "Ein Vertrag durf nur am 14. oder letzten Tag eines Monats enden."
            )

        return end_date

    def validate_hours(self, hours):
        """
        We check wether the provided value for hours is greater than zero.
        :param hours:
        :return: hours
        """
        if hours < 0:
            raise serializers.ValidationError(
                "Die Anzahl der Stunden muss größer 0 sein."
            )

        return hours
