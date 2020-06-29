# Generated by Django 2.2.13 on 2020-06-29 17:02

from django.db import migrations, models

import math


def hours_to_minutes(apps, schema_editor):
    # We have already renamed the field from `hours` to `minutes` We only need
    # to multiply the old value by 60 and round it for good measures.
    Contract = apps.get_model("api", "Contract")
    for contract in Contract.objects.all():
        contract.minutes = math.ceil(contract.minutes * 60)
        contract.save()


class Migration(migrations.Migration):

    dependencies = [("api", "0012_auto_20200629_1902")]

    operations = [
        migrations.AlterField(
            model_name="contract", name="minutes", field=models.PositiveIntegerField()
        ),
        migrations.RunPython(hours_to_minutes),
    ]
