import uuid
from django.db import models
from taggit.managers import TaggableManager


class User(models.Model):

    id = models.UUIDField(primary_key=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Contract(models.Model):

    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(
        to=User, related_name="contracts", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    hours = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=User, related_name="+", on_delete=models.CASCADE
    )  # No backwards relation to these Fields
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        to=User, related_name="+", on_delete=models.CASCADE
    )  # No backwards relation to these Fields


class Shift(models.Model):

    TYPE_CHOICES = (("st", "Shift"), ("sk", "Sick"), ("vn", "Vacation"))

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(to=User, related_name="shifts", on_delete=models.CASCADE)
    started = models.DateTimeField()
    stopped = models.DateTimeField()
    contract = models.ForeignKey(
        to=Contract, related_name="shifts", on_delete=models.CASCADE
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=2)
    note = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    was_reviewed = models.BooleanField(default=True)
    was_exported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
