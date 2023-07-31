from django import forms
from django.contrib import admin

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
from .models import Message


class DateOrderForm(forms.ModelForm):
    """
    Validate whether a validity start date and end date are in the correct order.
    """

    def clean(self):
        valid_from = self.cleaned_data.get("valid_from")
        valid_to = self.cleaned_data.get("valid_to")

        if valid_to is not None and valid_to < valid_from:
            error_message = "Ensure the end date is equal with or after the start date."
            self.add_error("valid_to", error_message)

        super(DateOrderForm, self).clean()


class MessageAdmin(admin.ModelAdmin):
    form = DateOrderForm
    list_display = ["id", "type", "en_title", "de_title", "valid_from", "valid_to"]


admin.site.register(Message, MessageAdmin)
