from django.contrib import admin

from api.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "email", "last_name", "created_at", "modified_at")


admin.site.register(User, UserAdmin)
