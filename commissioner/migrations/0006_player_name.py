# Generated by Django 5.0.12 on 2025-02-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commissioner", "0005_player_bet"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="name",
            field=models.CharField(max_length=64, null=True),
        ),
    ]
