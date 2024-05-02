# Generated by Django 4.2.9 on 2024-05-02 15:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuthKey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.UUIDField(
                        auto_created=True, default=uuid.uuid4, editable=False
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
