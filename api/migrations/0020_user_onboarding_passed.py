# Generated by Django 2.2.18 on 2022-04-25 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20210604_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='onboarding_passed',
            field=models.BooleanField(default=False),
        ),
    ]