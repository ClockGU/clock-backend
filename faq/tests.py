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
import pytest
from faq.models import Faq, FaqHeading
from faq.views import FaqsViewSet

# Create your tests here.
class TestFaq:
    @pytest.mark.django_db
    def test_show_in_clock_field(self):
        heading_true = FaqHeading.objects.create( show_in_clock=True, prio_level=1 )
        assert heading_true.show_in_clock == True

    @pytest.mark.django_db
    def test_show_in_clock_filter(self):
        heading_true = FaqHeading.objects.create( show_in_clock=True, prio_level=1 )
        heading_false = FaqHeading.objects.create( show_in_clock=False, prio_level=1 )

        faq_true = Faq.objects.create( faq_heading = heading_true, prioritization=1 )
        faq_false = Faq.objects.create( faq_heading = heading_false, prioritization=1 )

        view = FaqsViewSet()
        queryset = FaqsViewSet.get_clock_faqs(view)

        assert faq_true in queryset
        assert faq_false not in queryset

    @pytest.mark.django_db
    def test_show_in_supervisor_field(self):
        heading_true = FaqHeading.objects.create( show_in_supervisor=True, prio_level=1 )
        assert heading_true.show_in_supervisor == True

    @pytest.mark.django_db
    def test_show_in_supervisor_filter(self):
        heading_true = FaqHeading.objects.create( show_in_supervisor=True, prio_level=1 )
        heading_false = FaqHeading.objects.create( show_in_supervisor=False, prio_level=1 )

        faq_true = Faq.objects.create( faq_heading = heading_true, prioritization=1 )
        faq_false = Faq.objects.create( faq_heading = heading_false, prioritization=1 )

        view = FaqsViewSet()
        queryset = FaqsViewSet.get_supervisor_faqs(view)

        assert faq_true in queryset
        assert faq_false not in queryset
