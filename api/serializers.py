from calendar import monthrange

from more_itertools import pairwise
from dateutil.relativedelta import relativedelta
from django.db.models import DurationField, F, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from pytz import datetime, utc
from rest_framework import exceptions, serializers
from holidays import country_holidays

from api.models import ClockedInShift, Contract, Report, Shift, User
from api.utilities import (
    create_reports_for_contract,
    relativedelta_to_string,
    update_reports,
)


class TagsSerializerField(serializers.Field):
    """
    Custom Field to represent Tags within the ShiftSerializer.
    Tags are represented by a list of strings.
    """

    def to_representation(self, obj):
        return list(map(lambda x: x.name, obj.all()))

    def to_internal_value(self, data):
        return data


class TimedeltaField(serializers.Field):
    def to_representation(self, value):
        return relativedelta_to_string(
            relativedelta(seconds=value.total_seconds())
        )


class RestrictModificationModelSerializer(serializers.ModelSerializer):
    """
    This class, derived from ModelSerializer, is used as a base class for all Serializer classes within the project.
    The purpose of this baseclass is to assure that whatever a (possible) malicious User provides within the fields
    'user', 'created_by' or 'modified_by' is set to the user id given by the JWT Authentication.
    This solely refers to POST, PUT and PATCH methods and thereby prevent manipulation of other users content.
    """

    def add_user_id(self, request, data):
        user_id = request.user.id
        data["user"] = user_id
        data["created_by"] = user_id
        data["modified_by"] = user_id
        return data

    def to_internal_value(self, data):
        request = self.context["request"]

        if request.method in ["POST", "PUT"]:
            data = self.add_user_id(request, data)

        if request.method == "PATCH":
            # Not allowed keys "user" and "created_by" in a PATCH-Request.
            # Set "modified_by" to the user issuing the request
            data.pop("user", None)
            data.pop("created_by", None)
            data["modified_by"] = request.user.id

        return super(RestrictModificationModelSerializer, self).to_internal_value(data)


class UserSerializer(RestrictModificationModelSerializer):
    """
    Serializer only needed for GDPR-Export of User data.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "personal_number",
            "language",
            "dsgvo_accepted",
            "date_joined",
            "modified_at",
            "last_login",
            "is_superuser",
            "onboarding_passed",
        ]
        ref_name = "user-gdpr-serializers"


class DjoserUserSerializer(serializers.Serializer):
    class Meta:
        ref_name = "djoser-custom-serializer"

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "personal_number",
            "language",
            "dsgvo_accepted",
            "date_joined",
            "modified_at",
            "last_login",
            "is_superuser",
            "onboarding_passed",
        ]


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
        today = datetime.date.today()
        carryover_target_date = attrs.get("carryover_target_date")
        initial_carryover_minutes = attrs.get("initial_carryover_minutes")

        # Catches PUT
        if self.instance:
            # Catches PATCH
            if self.partial:
                start_date = attrs.get("start_date", self.instance.start_date)
                end_date = attrs.get("end_date", self.instance.end_date)
                carryover_target_date = attrs.get(
                    "carryover_target_date", self.instance.carryover_target_date
                )
                initial_carryover_minutes = attrs.get(
                    "initial_carryover_minutes", self.instance.initial_carryover_minutes
                )

            if Shift.objects.filter(
                    contract=self.instance, started__lt=start_date
            ).exists():
                raise serializers.ValidationError(
                    _(
                        "A contract's start date can not be modified"
                        "if shifts before this date exist."
                    )
                )
            if Shift.objects.filter(
                    contract=self.instance, started__gt=end_date
            ).exists():
                raise serializers.ValidationError(
                    _(
                        "A contract's end date can not be modified"
                        "if shifts after this date exist."
                    )
                )

            # check if new end date is more than 6 month apart from the old one
            if relativedelta(end_date, self.instance.end_date).months >= 6:
                raise serializers.ValidationError(
                    "A contract's end date can not be modified"
                    "extended for more than 6 months."
                )

        if start_date > end_date:
            raise serializers.ValidationError(
                _("The start date of a contract must be set before its end date.")
            )

        if end_date < today:
            raise serializers.ValidationError(
                _("A contract's end date must not be set in the past.")
            )

        if start_date > today:

            if not initial_carryover_minutes == 0:
                raise serializers.ValidationError(
                    _(
                        "The carry over for a contract starting in the future may only be 00:00."
                    )
                )

        if not start_date.replace(day=1) <= carryover_target_date < end_date:
            raise serializers.ValidationError(
                _(
                    "The month in which you want to start clocking must be set in-between the start and end date."
                )
            )

        if not carryover_target_date.day == 1:
            raise serializers.ValidationError(
                _(
                    "The date on which you want to start clocking must be the first of a month."
                )
            )

        return attrs

    def validate_start_date(self, start_date):
        """
        Check that the day of the start_date is the 1st or 16th day of the month.
        :param start_date:
        :return:
        """
        if start_date.day not in (1, 16):
            raise serializers.ValidationError(
                _("A contract must start on the 1st or 16th of a month.")
            )

        return start_date

    def validate_end_date(self, end_date):
        """
        Check that the contract ends either on the 15th or last day of a month.
        :param end_date:
        :return:
        """
        if end_date.day not in (15, monthrange(end_date.year, end_date.month)[1]):
            raise serializers.ValidationError(
                _("A contract must end on the 15th or last day of a month.")
            )

        return end_date

    def update(self, instance, validated_data):

        carryover_target_date_changed = bool(
            validated_data.get("carryover_target_date")
        )
        initial_carryover_minutes_changed = bool(
            validated_data.get("initial_carryover_minutes")
        )
        if not self.partial:
            carryover_target_date_changed = (
                    validated_data.get("carryover_target_date")
                    != instance.carryover_target_date
            )
            initial_carryover_minutes_changed = (
                    validated_data.get("initial_carryover_minutes")
                    != instance.initial_carryover_minutes
            )

        return_instance = super(ContractSerializer, self).update(
            instance, validated_data
        )

        if carryover_target_date_changed:
            # Delete all existing Reports
            Report.objects.filter(contract=instance).delete()
            # Recreate them.
            create_reports_for_contract(contract=instance)

        if carryover_target_date_changed or initial_carryover_minutes_changed:
            update_reports(instance, instance.carryover_target_date)

        return return_instance


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
            "was_reviewed": {"required": False},
            "locked": {"read_only": True},
        }

    def calculate_break(self, started: datetime, stopped: datetime, shifts_queryset):
        """
        Calculation of total breaks between shifts.

        @param started:
        @param stopped:
        @param shifts_queryset:
        @return:
        """
        if not shifts_queryset.exists():
            return datetime.timedelta(seconds=0)
        shifts_queryset = shifts_queryset.order_by("started")

        total_break = datetime.timedelta()

        for shift, shift_next in pairwise(shifts_queryset):
            total_break += shift_next.started - shift.stopped

        # new shift is after old shifts
        if started >= shifts_queryset.last().stopped:
            return (started - shifts_queryset.last().stopped) + total_break
        # new shift is before old shifts
        if stopped <= shifts_queryset.first().started:
            return (shifts_queryset.first().started - stopped) + total_break

        # new shift is in between old shifts
        return total_break - (stopped - started)

    def validate(self, data):
        started = data.get("started")
        stopped = data.get("stopped")
        contract = data.get("contract")
        shift_type = data.get("type")
        was_reviewed = data.get("was_reviewed", False)

        this_day = Shift.objects.filter(
            contract=contract,
            started__date=started,
        )

        vacation_sick_shifts_this_day = this_day.filter(
            type__in=('sk', 'vn')
        )

        if self.instance and (self.partial or self.context["request"].method == "PUT"):
            started = data.get("started", self.instance.started)
            stopped = data.get("stopped", self.instance.stopped)
            contract = data.get("contract", self.instance.contract)
            was_reviewed = data.get("was_reviewed", self.instance.was_reviewed)
            vacation_sick_shifts_this_day = vacation_sick_shifts_this_day.exclude(id=self.instance.id)

        if self.instance:
            uuid = self.instance.id
            this_day = this_day.exclude(id=uuid)

        new_worktime = stopped - started
        old_worktime = this_day.aggregate(
            total_work_time=Coalesce(
                Sum(F("stopped") - F("started"), output_field=DurationField()),
                datetime.timedelta(0),
            )
        )[
            "total_work_time"
        ]

        total_worktime = old_worktime + new_worktime
        total_break = self.calculate_break(started=started, stopped=stopped, shifts_queryset=this_day)

        if new_worktime + old_worktime > datetime.timedelta(hours=10):
            raise exceptions.ValidationError(
                _(
                    f"It is not allowed to save more than 10h total worktime per day "
                    f"(clocked: {new_worktime + old_worktime} vs allowed: {datetime.timedelta(hours=10)})"
                )
            )

        locked = Shift.objects.filter(
            contract=contract,
            started__month=started.month,
            started__year=started.year,
            locked=True,
        ).exists()

        # validate that date is not a sunday
        if started.date().weekday() == 6:
            raise serializers.ValidationError(
                _("Shifts are not allowed on sundays")
            )

        # validate feiertage/bank holiday is just clockable on a feiertag/bank holiday
        de_he_holidays = country_holidays('DE', subdiv='HE')
        if started.strftime("%d/%m/%Y") in de_he_holidays and shift_type is not 'bh':
            raise serializers.ValidationError(
                _("On holidays there can just be clocked shifts with type holiday/Feiertag ")
            )

        # validate that there is already one vacation or sick shift this day
        if vacation_sick_shifts_this_day.exists():
            raise serializers.ValidationError(
                _("There can just be one V/S Shift per day")
            )

        # validate that there is no standard shift this day if new shift is a vacation or sick shift
        if type in ('sk', 'vn'):
            other_shifts_this_day = Shift.objects.filter(
                contract=contract,
                started__year=started.year,
                started__month=started.month,
                started__day=started.day
            ).exists()
            if other_shifts_this_day:
                raise serializers.ValidationError(
                    _("Cannot add a vacation or sick shift to a workday with other shifts.")
                )

        # validate that started and stopped are on the same day
        if not (started.date() == stopped.date()):
            raise serializers.ValidationError(
                _("A shift must start and end on the same day.")
            )
        if started > stopped:
            raise serializers.ValidationError(
                _("The start of a shift must be set before its end.")
            )

        if not (contract.carryover_target_date <= started.date() <= contract.end_date):
            raise serializers.ValidationError(
                _(
                    "A shift must belong to a contract which is active on the respective date."
                )
            )

        if not (contract.carryover_target_date <= stopped.date() <= contract.end_date):
            raise serializers.ValidationError(
                _(
                    "A shift must belong to a contract which is active on the respective date."
                )
            )

        if total_worktime > datetime.timedelta(hours=9):
            # Needed break >= 45min in total
            if not this_day.exists() or total_break < datetime.timedelta(minutes=45):
                raise exceptions.ValidationError(
                    f"Total worktime ({total_worktime}) is > 9h and therefor is a break >= 45min needed, "
                    f"currently total break is {total_break}")

        if total_worktime > datetime.timedelta(hours=6):
            # Needed break >= 30min in total
            if not this_day.exists() or total_break < datetime.timedelta(minutes=30):
                raise exceptions.ValidationError(
                    f"Total worktime ({total_worktime}) is > 6h and therefor is a break >= 30min needed, "
                    f"currently total break is {total_break}")

        # If Shift is considered as scheduled
        if not was_reviewed:
            # A scheduled Shift has to start in the future
            if not started > datetime.datetime.now().astimezone(utc):
                raise serializers.ValidationError(
                    _("A scheduled shift must start or end in the future.")
                )
        else:
            if started > datetime.datetime.now().astimezone(utc):
                raise serializers.ValidationError(
                    _("A shift set in the future must be labeled as scheduled.")
                )
        # locked is read_only and marks whether a shift was exported and hence not modifyable anymore
        if locked:
            raise exceptions.PermissionDenied(
                _(
                    "A Shift can't be created or changed if the month has already been locked."
                )
            )
        return data

    def validate_contract(self, contract):
        if not (contract.user == self.context["request"].user):
            raise serializers.ValidationError(
                _("The contract object must be owned by the user creating the shift.")
            )

        return contract

    def validate_tags(self, tags):
        """
        Validate that the deserialization of the tags field is a list and
        that all values within this list are strings.
        :param tags:
        :return:
        """
        if not isinstance(tags, list):
            raise serializers.ValidationError(
                _(
                    "Tags must be represented by a list and not by {}.".format(
                        type(tags)
                    )
                )
            )

        if not all(map(lambda x: isinstance(x, str), tags)):
            raise serializers.ValidationError(_("Tags must be strings."))

        return tags

    def create(self, validated_data):
        """
        Customization of the derived create method.
        It adds the utility to create Tags.
        :param validated_data:
        :return:
        """
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
        # To update the old report if we change the contract we need
        # to check this
        contract_changed = bool(validated_data.get("contract"))
        if not self.partial:
            contract_changed = validated_data.get("contract") != instance.contract
        # keep track of possibly old contract
        # and old started value
        orig_contract = instance.contract
        orig_started = instance.started
        tags = validated_data.pop("tags", None)
        updated_object = super(ShiftSerializer, self).update(instance, validated_data)

        if isinstance(tags, list):
            updated_object.tags.set(*tags)

        if contract_changed:
            update_reports(orig_contract, orig_started.date().replace(day=1))

        return updated_object


class ClockedInShiftSerializer(RestrictModificationModelSerializer):
    class Meta:
        model = ClockedInShift
        fields = "__all__"
        extra_kwargs = {
            # Will be set automatically by the Model
            "created_at": {"required": False},
            "modified_at": {"required": False},
            "created_by": {"write_only": True},
            "modified_by": {"write_only": True},
            "user": {"write_only": True},
        }

    def validate(self, data):
        started = data.get("started")
        contract = data.get("contract")
        vacation_sick_shifts_this_day = Shift.objects.filter(
            contract=contract,
            started__date=started,
            type__in=('sk', 'vn')
        )

        # validate that there is not already one vacation or sick shift this day
        if vacation_sick_shifts_this_day.exists():
            raise serializers.ValidationError(
                _("Live clocking is not allowed on days where already a vacation or a sick shift is clocked.")
            )

        return data

    def validate_started(self, started):
        # no Live clocking on Feiertage/holidays
        de_he_holidays = country_holidays('DE', subdiv='HE')
        if started.strftime("%d/%m/%Y") in de_he_holidays:
            raise serializers.ValidationError(
                _("Live clocking is not allowed on feiertage/ bank holidays.")
            )

        # no live clocking on a sunday
        if started.date().weekday() == 6:
            raise serializers.ValidationError(
                _("Live clocking is not allowed on sundays")
            )

        return started

    def validate_contract(self, contract):
        if not (contract.user == self.context["request"].user):
            raise serializers.ValidationError(
                _("The contract must be owned by the user creating the shift.")
            )

        return contract


class ReportSerializer(RestrictModificationModelSerializer):
    """
    This Serializer class does not provide any custom validation since it is only used within a
    ReadOnlyViewSet and therefore will never perform a create or update.
    """

    debit_worktime = TimedeltaField()
    worktime = TimedeltaField()
    carryover_previous_month = TimedeltaField()
    carryover = TimedeltaField()

    class Meta:
        model = Report
        fields = "__all__"
        extra_kwargs = {
            # Will be set automatically by the Model
            "created_at": {"required": False},
            "modified_at": {"required": False},
            "created_by": {"write_only": True},
            "modified_by": {"write_only": True},
            "user": {"write_only": True},
        }
