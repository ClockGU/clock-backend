# Generated by Django 2.2.28 on 2023-03-30 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_contract_carryover_target_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]