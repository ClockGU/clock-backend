# Generated by Django 2.2 on 2020-04-27 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200427_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='was_exported',
            new_name='locked',
        ),
    ]
