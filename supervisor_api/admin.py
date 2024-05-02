from django.contrib import admin
from .models import AuthKey
# Register your models here.

admin.site.register(AuthKey, admin.ModelAdmin)