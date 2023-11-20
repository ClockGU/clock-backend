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
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Faq(models.Model):
    de_question = models.CharField(max_length=200, verbose_name="Faq-question german")

    de_answer = models.TextField(max_length=500, verbose_name="Faq-answer german")

    en_question = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Faq-question english"
    )

    en_answer = models.TextField(
        max_length=500, blank=True, null=True, verbose_name="Faq-answer english"
    )

    prioritization = models.FloatField(
        default=0,
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name="Prio (0.0 - 10.0)",
    )
