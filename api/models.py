import uuid
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.base_user import BaseUserManager
from django import forms


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        email,
        password,
        first_name="",
        last_name="",
        personal_number="",
        username="",
        **extra_fields
    ):
        """
        Create and save a user with the given username, email, password, first_name, last_name and personal_number.
        """

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            personal_number=personal_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email="",
        first_name="",
        last_name="",
        personal_number="",
        password="",
        username="",
        **extra_fields
    ):
        if not email:
            raise ValueError("The field 'email' is required.")
        if not first_name:
            raise ValueError("The field 'first_name' is required.")
        if not last_name:
            raise ValueError("The field 'last_name' is required.")
        if not personal_number:
            raise ValueError("The field 'personal_number' is required.")
        if not password:
            raise ValueError("The field 'password' is required.")
        # We always set the provided username to the user's email
        username = email
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            personal_number=personal_number,
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    username = models.CharField(max_length=151, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)  # Firstname is required
    last_name = models.CharField(max_length=100)  # Lastname is required
    personal_number = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "personal_number"]

    objects = CustomUserManager()


class Contract(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
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
    tags = TaggableManager(blank=True, through=UUIDTaggedItem)
    was_reviewed = models.BooleanField(default=True)
    was_exported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)


class Report(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    month_year = models.DateField()
    hours = models.DurationField()
    contract = models.ForeignKey(
        to=Contract, related_name="reports", on_delete=models.CASCADE
    )
    user = models.ForeignKey(to=User, related_name="reports", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(to=User, related_name="+", on_delete=models.CASCADE)
