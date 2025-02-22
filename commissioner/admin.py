from django.contrib import admin

from commissioner.models import Race, State, Track

# Register your models here.


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    display_name = "Races"


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    display_name = "Tracks"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    display_name = "States"
