# Generated by Django 5.0.2 on 2024-03-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_entry_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='comments',
            field=models.CharField(blank=True, default='test comment', max_length=255),
        ),
    ]
