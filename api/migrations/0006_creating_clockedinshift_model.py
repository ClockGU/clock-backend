# Generated by Django 2.2 on 2019-11-07 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_support_uuid_pk_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClockedInShift',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('started', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clocked_in_shift', to='api.Contract')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clocked_in_shift', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
