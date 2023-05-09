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
    de_text = models.TextField(default="", blank=True, verbose_name="text (Markdown)")
    en_title = models.CharField(max_length=100, default="", blank=True)
    en_text = models.TextField(default="", blank=True, verbose_name="text (Markdown)")
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.en_title
