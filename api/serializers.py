import json

from rest_framework import serializers
from calendar import monthrange
from api.models import Contract, Shift
from rest_framework.request import QueryDict


class TagsSerializerField(serializers.Field):
    def to_representation(self, obj):
        return list(map(lambda x: x.name, obj.all()))

    def to_internal_value(self, data):
        return json.loads(data)


class RestrictModificationModelSerializer(serializers.ModelSerializer):
    def add_user_id(self, request, data):
        user_id = request.user.id
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
            data["modified_by"] = request.user.id

        return super(RestrictModificationModelSerializer, self).to_internal_value(data)


class ContractSerializer(RestrictModificationModelSerializer):
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


class ShiftSerializer(RestrictModificationModelSerializer):

    tags = TagsSerializerField()

    class Meta:
        model = Shift
        fields = "__all__"
        extra_kwargs = {
            # Will be set automatically by the Model
            "created_at": {"required": False},
            # Will be set automatically by the Model
            "modified_at": {"required": False},
            "created_by": {"write_only": True},
            "modified_by": {"write_only": True},
            "user": {"write_only": True},
            "was_reviewed": {"read_only": True},
            "was_exported": {"read_only": True},
        }

    def validate(self, attrs):
        print(attrs)
        assert attrs.get("tags")
        started = attrs.get("started")
        stopped = attrs.get("stopped")
        contract = attrs.get("contract")

        if self.instance and self.partial:
            started = attrs.get("started", self.instance.started)
            stopped = attrs.get("stopped", self.instance.stopped)
            contract = attrs.get("contract", self.instance.contract)

        # validate that started and stopped are on the same day
        if not (started.date() == stopped.date()):
            raise serializers.ValidationError(
                "Eine Schicht muss an dem gleichen Tag enden an dem sie angefangen hat."
            )
        if started > stopped:
            raise serializers.ValidationError(
                "Der Beginn einer Schicht muss vor deren Ende leigen."
            )

        if not (contract.start_date < started.date() < contract.end_date):
            raise serializers.ValidationError(
                "Eine Schicht muss zu einem zu dem Zeitpunkt laufenden Vertrag gehören."
            )

        return attrs

    def validate_contract(self, contract):
        if not (contract.user == self.context["request"].user):
            raise serializers.ValidationError(
                "Das Vertragsobjekt muss dem User gehören der die Schicht erstellt."
            )

        return contract

    def validate_tags(self, tags):
        assert tags
        if not isinstance(tags, list):
            raise serializers.ValidationError(
                "Tags müssen als Liste und nicht als {} dargestellt werden.".format(
                    type(tags)
                )
            )

        if not all(map(lambda x: isinstance(x, str), tags)):
            raise serializers.ValidationError("Tags dürfen nur strings sein.")

        return tags

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        created_object = super(ShiftSerializer, self).create(validated_data)
        if tags:
            assert isinstance(tags, list)
            created_object.tags.set(*tags)

        return created_object

    def update(self, instance, validated_data):
        """
        On an update, we override the tags.
        Therefore all previous tags have to be provided to 'add' a new one.
        Example:

        old tags --> ['tag1', 'tag2']

        new tags --> ['tag1', 'tag2', 'tag3']

        provided tags to achieve this : ['tag1', 'tag2', 'tag3']

        :param instance:
        :param validated_data:
        :return:
        """
        tags = validated_data.pop("tags", None)
        updated_object = super(ShiftSerializer, self).update(instance, validated_data)
        if tags:
            assert isinstance(tags, list)
            updated_object.tags.set(*tags)
        return updated_object
