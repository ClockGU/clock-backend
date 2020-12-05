from api.filters import ShiftFilterSet


class TestShiftFilterSet:
    def test_was_reviewed_filter(self):
        assert "was_reviewed" in ShiftFilterSet._meta.fields

    def test_was_reviewed_lookups(self):
        assert ShiftFilterSet._meta.fields["was_reviewed"] == ["exact"]

    def test_started_filter(self):
        assert "started" in ShiftFilterSet._meta.fields

    def test_started_lookups(self):
        assert ShiftFilterSet._meta.fields["started"] == ["exact", "lte"]
