# Generated by Django 2.2.13 on 2020-12-27 15:19

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_add_dsgvo_accepted_field_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='last_used',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
