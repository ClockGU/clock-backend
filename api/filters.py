import django_filters

from api.models import Shift


class ShiftFilterSet(django_filters.FilterSet):
    class Meta:
        model = Shift
        fields = {"started": ["exact", "lte"], "was_reviewed": ["exact"]}
