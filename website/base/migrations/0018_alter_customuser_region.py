# Generated by Django 5.0.2 on 2024-04-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_entry_receptionist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='region',
            field=models.CharField(choices=[('Nairobi HQ', 'Nairobi HQ'), ('Coast', 'Coast'), ('Rift Valley', 'Rift Valley'), ('Kisumu', 'Kisumu'), ('Estern', 'Estern')], max_length=100),
        ),
    ]
