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
from calendar import monthrange
from datetime import date

from django import template

register = template.Library()


@register.filter
def cut_year(date_str):
    return date_str[0 : date_str.rindex(".")] + "."


@register.simple_tag
def get_calendar(year, month):
    """
    Provide an iterable which consists of the days of a month as strings.
    :param year:
    :param month:
    :return:
    """
    for i in range(1, monthrange(year, month)[1] + 1):
        yield date(year, month, i).strftime("%d.%m.%Y")


@register.simple_tag
def get_dict_value(dictionary, key):
    """
    Mimics the .get() method of a Dictionary.
    :param key:
    :return:
    """
    return dictionary.get(key)
