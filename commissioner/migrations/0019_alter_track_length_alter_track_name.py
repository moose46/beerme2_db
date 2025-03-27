# Generated by Django 5.0.12 on 2025-03-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commissioner", "0018_alter_track_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="track",
            name="length",
            field=models.DecimalField(
                blank=True, decimal_places=4, default=0.0, max_digits=5
            ),
        ),
        migrations.AlterField(
            model_name="track",
            name="name",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
