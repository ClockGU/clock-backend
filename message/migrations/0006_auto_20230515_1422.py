# Generated by Django 2.2.28 on 2023-05-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_auto_20230509_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='de_text',
            field=models.TextField(blank=True, default='', verbose_name='de_text (Markdown)'),
        ),
        migrations.AlterField(
            model_name='message',
            name='en_text',
            field=models.TextField(blank=True, default='', verbose_name='en_text (Markdown)'),
        ),
    ]
