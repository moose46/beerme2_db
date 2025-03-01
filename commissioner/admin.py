from django.contrib import admin

from commissioner.models import (
    Bet,
    Driver,
    Player,
    Race,
    RaceResult,
    ScoreBoard,
    State,
    Team,
    Track,
)

# Register your models here.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    display_name = "Races"
    ordering = ["name"]


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    display_name = "Races"
    list_display = ["name", "race_date", "track"]
    ordering = ["-race_date"]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    display_name = "Race Picks"


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    display_name = "Bets"
    list_display = ["player", "driver", "track_name", "finish", "race_date"]
    ordering = ["race", "player"]

    def race_date(self, instance):
        return instance.race.race_date

    def track_name(self, instance):
        return instance.race.track.name


@admin.register(RaceResult)
class RaceResultsAdmin(admin.ModelAdmin):
    display_name = "Race Results"


@admin.register(ScoreBoard)
class ScoreBoardAdmin(admin.ModelAdmin):
    display_name = "Race Results"


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    display_name = "Tracks"
    ordering = ["name"]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    display_name = "States"
    ordering = ["name"]


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    display_name = "Drivers"
    list_display = ["name", "team"]
    ordering = ["name"]
