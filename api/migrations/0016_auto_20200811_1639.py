# Generated by Django 2.2.13 on 2020-08-11 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20200711_2109'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('month_year', 'contract')},
        ),
    ]