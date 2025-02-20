# Generated by Django 5.1.6 on 2025-02-19 18:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_read_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
