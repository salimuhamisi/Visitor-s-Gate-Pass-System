# Generated by Django 5.0.2 on 2024-05-07 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_alter_group_created_at_alter_groupmember_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='receptionist',
            field=models.ForeignKey(default='Receptionist', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
