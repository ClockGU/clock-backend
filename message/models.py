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
from datetime import date

from django.db import models


class Message(models.Model):
    """
    Model for a message that is displayed to the users when the app starts.
    """

    MTYPE_CHOICES = [
        ("NO", "Notice"),
        ("UD", "Update"),
        ("CL", "Changelog"),
        ("WN", "Warning"),
        ("TP", "Tipp"),
    ]

    type = models.CharField(max_length=2, choices=MTYPE_CHOICES)
    de_title = models.CharField(max_length=100)
    de_text = models.TextField(
        default="", blank=True, verbose_name="de_text (Markdown)"
    )
    en_title = models.CharField(max_length=100, default="", blank=True)
    en_text = models.TextField(
        default="", blank=True, verbose_name="en_text (Markdown)"
    )
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.en_title
