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
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from api.models import ClockedInShift, Contract, Report, Shift

# Removed User import and UserAdmin class since user management is external


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_user_id",
        "name",
        "minutes",
        "start_date",
        "end_date",
        "modified_at",
    )
    list_per_page = 100
    ordering = ("-modified_at",)
    search_fields = ("user_id", "name", "id")
    list_filter = (
        "start_date",
        "end_date",
    )

    def display_user_id(self, obj):
        """
        Display the user_id since we no longer have direct user access
        """
        return str(obj.user_id)

    display_user_id.short_description = "User ID"


admin.site.register(Contract, ContractAdmin)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ("id", "display_user_id", "started", "stopped", "locked", "modified_at")
    list_per_page = 200
    ordering = ("-modified_at",)
    search_fields = ("user_id", "contract__name", "id")
    list_filter = ("started", "type", "locked")

    def display_user_id(self, obj):
        """
        Display the user_id since we no longer have direct user access
        """
        return str(obj.user_id)

    display_user_id.short_description = "User ID"


admin.site.register(Shift, ShiftAdmin)


class ClockedInShiftAdmin(admin.ModelAdmin):
    list_display = ("id", "display_user_id", "link_contract", "created_at", "duration")

    def display_user_id(self, obj):
        """
        Display the user_id since we no longer have direct user access
        """
        return str(obj.user_id)

    def link_contract(self, obj):
        """
        Creates a link to the corresponding Contract object to display in the columns.
        """
        contract = obj.contract
        url = reverse("admin:api_contract_change", args=[contract.pk])
        return format_html('<a href="{}">{}</a>', url, contract.pk)

    def duration(self, obj):
        started = obj.started
        now = timezone.now()

        sec = (now - started).seconds
        hours = sec // 3600
        minutes = (sec // 60) - (hours * 60)

        return f"{hours:02d}:{minutes:02d}"

    display_user_id.short_description = "User ID"
    link_contract.short_description = "contract"
    duration.short_description = "duration"


admin.site.register(ClockedInShift, ClockedInShiftAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_user_id",
        "format_date",
        "link_contract",
        "created_at",
        "modified_at",
    )
    search_fields = ("user_id", "contract__name", "id")
    list_filter = ("month_year",)

    def format_date(self, obj):
        date = obj.month_year
        return date.strftime("%B %Y")

    def display_user_id(self, obj):
        """
        Display the user_id since we no longer have direct user access
        """
        return str(obj.user_id)

    def link_contract(self, obj):
        """
        Creates a link to the corresponding Contract object to display in the columns.
        """
        contract = obj.contract
        url = reverse("admin:api_contract_change", args=[contract.pk])
        return format_html('<a href="{}">{}</a>', url, contract.pk)

    format_date.short_description = "date"
    display_user_id.short_description = "User ID"
    link_contract.short_description = "contract"


admin.site.register(Report, ReportAdmin)
