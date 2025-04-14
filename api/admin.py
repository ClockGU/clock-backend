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
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from api.models import ClockedInShift, Contract, Report, Shift, User


class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "date_joined",
        "modified_at",
    )
    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[1][1]["fields"] += (
        "language",
        "personal_number",
        "dsgvo_accepted",
        "onboarding_passed",
        "is_supervisor",
    )
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined",)


admin.site.register(User, UserAdmin)


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "link_user",
        "name",
        "minutes",
        "start_date",
        "end_date",
        "modified_at",
    )
    list_per_page = 100
    ordering = ("-modified_at",)
    search_fields = ("user__first_name", "user__last_name", "user__id", "user__mail")
    list_filter = (
        "start_date",  
        "end_date",
    )

    def link_user(self, obj):
        """
        Creates a link to the corresponding User object to display in the columns.
        :param obj:
        :return: string
        """
        user = obj.user
        url = reverse("admin:api_user_change", args=[user.pk])
        return format_html('<a href="{}">{}</a>', url, user.pk)

    link_user.short_description = "user"


admin.site.register(Contract, ContractAdmin)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ("id", "link_user", "started", "stopped", "locked", "modified_at")
    list_per_page = 200
    ordering = ("-modified_at",)
    list_filter = (
        "user",
        "contract",
        "started",
    )

    def link_user(self, obj):
        """
        Creates a link to the corresponding User object to display in the columns.
        :param obj:
        :return: string
        """
        user = obj.user
        url = reverse("admin:api_user_change", args=[user.pk])
        return format_html('<a href="{}">{}</a>', url, user.pk)

    link_user.short_description = "user"

admin.site.register(Shift, ShiftAdmin)


class ClockedInShiftAdmin(ShiftAdmin):
    list_display = ("id", "link_user", "link_contract", "created_at", "duration")

    def link_contract(self, obj):
        """
        Creates a link to the corresponding Contract object to display in the columns.
        :param obj:
        :return: string
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

    link_contract.short_description = "contract"
    duration.short_description = "duration"


admin.site.register(ClockedInShift, ClockedInShiftAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "link_user",
        "format_date",
        "link_contract",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "month_year",
        "user",
        "contract"
    )

    def format_date(self, obj):
        date = obj.month_year

        return date.strftime("%B %Y")

    def link_user(self, obj):
        """
        Creates a link to the corresponding User object to display in the columns.
        :param obj:
        :return: string
        """
        user = obj.user
        url = reverse("admin:api_user_change", args=[user.pk])
        return format_html('<a href="{}">{}</a>', url, user.pk)

    def link_contract(self, obj):
        """
        Creates a link to the corresponding Contract object to display in the columns.
        :param obj:
        :return: string
        """
        contract = obj.contract
        url = reverse("admin:api_contract_change", args=[contract.pk])
        return format_html('<a href="{}">{}</a>', url, contract.pk)

    format_date.short_description = "date"
    link_user.short_description = "user"
    link_contract.short_description = "contract"


admin.site.register(Report, ReportAdmin)
