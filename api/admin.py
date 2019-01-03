from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from api.models import User, Contract


class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "email", "last_name", "created_at", "modified_at")


admin.site.register(User, UserAdmin)


class ContractAdmin(admin.ModelAdmin):

    list_display = ("id", "link_user", "name", "hours", "created_at", "modified_at")

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
