# Generated by Django 5.0.12 on 2025-02-28 19:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commissioner", "0011_scoreboard_race"),
    ]

    operations = [
        migrations.AlterField(
            model_name="race",
            name="race_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
