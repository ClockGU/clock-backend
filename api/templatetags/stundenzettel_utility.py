from django import template
from calendar import monthrange
from datetime import date

register = template.Library()


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
