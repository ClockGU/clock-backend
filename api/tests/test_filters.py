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
