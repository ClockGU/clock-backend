# Generated by Django 2.2.28 on 2023-03-30 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_make_valid_to_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('NO', 'Notice'), ('UD', 'Update'), ('CL', 'Changelog'), ('WN', 'Warning'), ('TP', 'Tipp')], max_length=2),
        ),
    ]