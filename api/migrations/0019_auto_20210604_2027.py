# Generated by Django 2.2.13 on 2021-06-04 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_contract_last_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='type',
            field=models.CharField(choices=[('st', 'Shift'), ('sk', 'Sick'), ('vn', 'Vacation'), ('bh', 'Bank Holiday')], max_length=2),
        ),
    ]
