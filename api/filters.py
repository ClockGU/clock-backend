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
