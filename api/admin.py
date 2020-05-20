from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from api.models import Contract, Report, Shift, User, ClockedInShift


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
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined",)


admin.site.register(User, UserAdmin)


class ContractAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "link_user",
        "name",
        "hours",
        "start_date",
        "end_date",
        "modified_at",
    )
    list_per_page = 100
    ordering = ("-modified_at",)

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
