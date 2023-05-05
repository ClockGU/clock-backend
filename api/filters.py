import django_filters

from api.models import Shift


class ShiftFilterSet(django_filters.FilterSet):
    contract = django_filters.UUIDFilter(field_name="contract", lookup_expr="exact")

    year = django_filters.NumberFilter(field_name="started", lookup_expr="year")
    month = django_filters.NumberFilter(field_name="started", lookup_expr="month")

    class Meta:
        model = Shift
        fields = ["started", "contract"]


class ReportFilterSet(django_filters.FilterSet):
    contract = django_filters.UUIDFilter(field_name="contract", lookup_expr="exact")
    month_year__gte = django_filters.DateFilter(
        field_name="month_year", lookup_expr="gte"
    )
