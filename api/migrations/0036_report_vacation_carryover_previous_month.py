import datetime

from django.db import migrations, models


def populate_vacation_carryover(apps, schema_editor):
    from django.db.models.signals import post_save

    from api.models import Contract, Report
    from api.utilities import send_reports_through_websocket, update_reports

    post_save.disconnect(
        send_reports_through_websocket,
        sender=Report,
        dispatch_uid="send_reports_through_websocket",
    )
    try:
        for contract in Contract.objects.order_by("start_date"):
            update_reports(contract, contract.start_date.replace(day=1))
    finally:
        post_save.connect(
            send_reports_through_websocket,
            sender=Report,
            dispatch_uid="send_reports_through_websocket",
        )


def reverse_populate_vacation_carryover(apps, schema_editor):
    Report = apps.get_model("api", "Report")
    Report.objects.all().update(vacation_carryover_previous_month=datetime.timedelta(0))


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0035_report_carryover_previous_month"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="vacation_carryover_previous_month",
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.RunPython(
            populate_vacation_carryover, reverse_populate_vacation_carryover
        ),
    ]