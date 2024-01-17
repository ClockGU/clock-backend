# Generated by Django 4.1.13 on 2024-01-17 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0028_contract_initial_vacation_carryover_minutes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="worktime_model_name",
            field=models.CharField(
                choices=[("studEmp", "Studentische Hilfskraft")],
                default="studEmp",
                max_length=200,
                verbose_name="Validierungsklasse",
            ),
            preserve_default=False,
        ),
    ]
