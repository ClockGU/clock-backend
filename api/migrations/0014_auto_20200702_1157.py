# Generated by Django 2.2.13 on 2020-07-02 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20200629_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('de', 'Deutsch'), ('en', 'English')], default='de', max_length=2),
        ),
    ]
