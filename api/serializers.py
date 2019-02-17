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
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if self.instance and self.partial:
            start_date = attrs.get("start_date", self.instance.start_date)
            end_date = attrs.get("end_date", self.instance.end_date)

        if start_date > end_date:
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

    def add_user_id(self, request, data):
        user_id = request.user_id
        data["user"] = user_id
        data["created_by"] = user_id
        data["modified_by"] = user_id
        return data

    def to_internal_value(self, data):
        request = self.context["request"]
        data = data.dict()
        if request.method in ["POST", "PUT"]:
            data = self.add_user_id(request, data)

        if request.method == "PATCH":
            # Not allowed keys "user" and "created_by" in a PATCH-Request.
            # Set "modified_by" to the user issuing the request
            data.pop("user", None)
            data.pop("created_by", None)
            data["modified_by"] = request.user_id

        return super(ContractSerializer, self).to_internal_value(data)
