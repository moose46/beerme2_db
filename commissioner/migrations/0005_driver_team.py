# Generated by Django 5.0.12 on 2025-02-26 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commissioner", "0004_remove_driver_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="commissioner.team",
            ),
        ),
    ]
