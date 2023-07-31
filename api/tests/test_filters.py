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

from api.filters import ShiftFilterSet


class TestShiftFilterSet:
    def test_contract_filter(self):
        assert "contract" in ShiftFilterSet.get_filters()

    def test_year_filter(self):
        assert "year" in ShiftFilterSet.get_filters()

    def test_month_filter(self):
        assert "month" in ShiftFilterSet.get_filters()

    def test_contract_lookups(self):
        filter = ShiftFilterSet.get_filters().get("contract")
        assert isinstance(filter, django_filters.UUIDFilter)
        assert filter.field_name == "contract"
        assert filter.lookup_expr == "exact"

    def test_year_lookups(self):
        filter = ShiftFilterSet.get_filters().get("year")
        assert isinstance(filter, django_filters.NumberFilter)
        assert filter.field_name == "started"
        assert filter.lookup_expr == "year"

    def test_month_lookups(self):
        filter = ShiftFilterSet.get_filters().get("month")
        assert isinstance(filter, django_filters.NumberFilter)
        assert filter.field_name == "started"
        assert filter.lookup_expr == "month"
