# Generated by Django 5.0.12 on 2025-02-27 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("commissioner", "0007_remove_driver_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="race",
            name="website",
        ),
    ]
