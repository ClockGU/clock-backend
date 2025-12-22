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
from django.utils.translation import gettext_lazy as _

from api.models import ClockedInShift, Contract, Report, Shift, User


class ShiftMonthYearFilter(admin.SimpleListFilter):
    """
    Filter for Shifts by month and year.
    """

    title = _("Month and Year")
    parameter_name = "month"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        """
        return (
            ("1", _("January")),
            ("2", _("February")),
            ("3", _("March")),
            ("4", _("April")),
            ("5", _("May")),
            ("6", _("June")),
            ("7", _("July")),
            ("8", _("August")),
            ("9", _("September")),
            ("10", _("October")),
            ("11", _("November")),
            ("12", _("December")),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query string.
        """
        if self.value():
            month = self.value()
            year = request.GET.get("year", None)

            if year:
                return queryset.filter(started__month=month, started__year=year)
            return queryset.filter(started__month=month)
        return queryset


class YearFilter(admin.SimpleListFilter):
    """
    Filter for Shifts by year.
    """

    title = _("Year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples with years from 2020 to current year + 1.
        """
        current_year = timezone.now().year
        years = [(str(year), str(year)) for year in range(2020, current_year + 2)]
        return years

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query string.
        """
        if self.value():
            year = self.value()
            month = request.GET.get("month", None)

            if month:
                return queryset.filter(started__month=month, started__year=year)
            return queryset.filter(started__year=year)
        return queryset


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
    search_fields = ("user__first_name", "user__last_name", "user__id", "user__email")
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


@admin.action(description="Unlock selected shifts")
def unlock_shifts_action(modeladmin, request, queryset):
    queryset.update(locked=False)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ("id", "link_user", "started", "stopped", "locked", "modified_at")
    list_per_page = 200
    ordering = ("-modified_at",)
    search_fields = (
        "user__id",
        "contract__id",
        "contract__reference",
        "user__first_name",
        "user__last_name",
    )
    list_filter = (
        ShiftMonthYearFilter,
        YearFilter,
    )
    actions = [unlock_shifts_action]

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
    search_fields = ("user", "contract")
    list_filter = ("month_year",)

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
