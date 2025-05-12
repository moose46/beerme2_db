from datetime import date

from django.contrib import admin

from commissioner.models import (
    Bet,
    Driver,
    DriverCurrentTeam,
    Player,
    Race,
    RaceResult,
    RacingSeries,
    ScoreBoard,
    State,
    Team,
    Track,
    TrackType,
)

# Register your models here.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    display_name = "Races"
    ordering = ["name"]


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    display_name = "Races"
    list_display = ["race_date", "track_name", "road_course", "reload"]
    search_fields = ["track__name"]
    ordering = ["-race_date"]

    # date_hierarchy = "race_date"
    def track_name(self, instance):
        return instance.track.name

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        try:
            search_term_as_date = int(search_term)
        except ValueError:
            pass
        else:
            # https://docs.djangoproject.com/en/5.1/topics/db/queries/
            queryset |= self.model.objects.filter(race_date__year=search_term_as_date)
        return queryset, may_have_duplicates


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    display_name = "Race Picks"


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    display_name = "Bets"
    list_display = ["player", "driver", "track_name", "finish", "race_date"]
    ordering = ["-race", "player"]

    def race_date(self, instance):
        return instance.race.race_date

    def track_name(self, instance):
        return instance.race.track.name


@admin.register(RaceResult)
class RaceResultsAdmin(admin.ModelAdmin):
    display_name = "Race Results"
    list_display = ["race", "driver", "finish_pos", "start_pos", "track_name"]
    ordering = ["-race__race_date", "finish_pos"]

    search_fields = [
        "race__track__name",
    ]

    def track_name(self, instance):
        return instance.race.track.name

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, may_have_duplicates = super().get_search_results(
    #         request,
    #         queryset,
    #         search_term,
    #     )
    #     try:
    #         search_term_as_int = int(search_term)
    #     except ValueError:
    #         print(search_term)
    #         # pass
    #         queryset = self.model.objects.filter(
    #             race__track__name__icontains=search_term
    #         )
    #     else:
    #         # https://docs.djangoproject.com/en/5.1/topics/db/queries/
    #         queryset = self.model.objects.filter(finish_pos__lte=search_term_as_int)

    #     return queryset, may_have_duplicates


@admin.register(ScoreBoard)
class ScoreBoardAdmin(admin.ModelAdmin):
    display_name = "Race Results"


@admin.register(TrackType)
class TrackTypeAdmin(admin.ModelAdmin):
    display_name = "Race Track Configuration"
    ordering = ["name"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    display_name = "Tracks"
    list_display = ["name", "track_type"]
    ordering = ["name"]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    display_name = "States"
    ordering = ["name"]


class DriverCurrentTeamInLine(admin.TabularInline):
    model = Driver.teams.through


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    display_name = "Drivers"
    inlines = [DriverCurrentTeamInLine]
    list_display = [
        "name",
        "salary",
    ]
    ordering = ["name"]


@admin.register(DriverCurrentTeam)
class DriverCurrentTeamAdmin(admin.ModelAdmin):
    display_name = "Team Driver Timeline"
    list_display = ["driver", "team", "racing_series"]
    ordering = ["driver__name"]


@admin.register(RacingSeries)
class RacingSeriesAdmin(admin.ModelAdmin):
    display_name = "Team Driver Timeline"
