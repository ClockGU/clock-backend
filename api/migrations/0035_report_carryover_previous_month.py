import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0034_contract_reference"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="carryover_previous_month",
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
