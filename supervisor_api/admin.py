from django.contrib import admin

from .models import AuthKey


# Register your models here.
class AuthKeyAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = ("id", "email", "created_at")


admin.site.register(AuthKey, AuthKeyAdmin)
