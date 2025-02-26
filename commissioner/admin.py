from django.contrib import admin

from commissioner.models import (
    Bet,
    Driver,
    Player,
    Race,
    RaceResult,
    State,
    Team,
    Track,
)

# Register your models here.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    display_name = "Races"


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    display_name = "Races"


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    display_name = "Race Picks"


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    display_name = "Bets"


@admin.register(RaceResult)
class RaceResultsAdmin(admin.ModelAdmin):
    display_name = "Race Results"


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    display_name = "Tracks"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    display_name = "States"


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    display_name = "Drivers"
    list_display = ["name"]
    ordering = ["name"]
