import string
from datetime import date
from enum import unique
from tkinter import CASCADE

import django.utils
import django.utils.timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Deferrable, UniqueConstraint
from pyexpat import model


# Create your models here.
class Base(models.Model):
    """
    Abstract base model for common fields.

    Provides common fields such as createdAt, user, and updatedAt for other models to inherit.
    """

    createdAt = models.DateTimeField("date created", auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    updatedAt = models.DateTimeField("date last updated", auto_now=True, null=True)

    class Meta:
        abstract = True


class Player(Base):
    name = models.CharField(max_length=64, null=True, unique=True)
    beers = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class State(Base):
    name = models.CharField(max_length=32, unique=True)
    country = models.CharField(max_length=32, default="USA", null=True)

    def __str__(self) -> str:
        return string.capwords(self.name)

    @property
    def state_name(self):
        return string.capwords(self.name)

    class META:
        unique = "name"
        ordering = "name"


class Team(Base):
    """
    Represents a racing team.

    This model stores information about a racing team, including its name.
    """

    name = models.CharField(max_length=32, unique=True)
    website = models.URLField(max_length=128, null=True, unique=True)

    def __str__(self):
        return self.name

    class META:
        ordering = ["name"]


class Track(Base):
    name = models.CharField(max_length=32, unique=True)
    short_name = models.CharField(max_length=16, null=True, default="N/A")
    website = models.URLField(null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    length = models.DecimalField(
        decimal_places=2, default=0.00, max_digits=2, blank=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )  # Validators should be a list

    def __str__(self) -> str:
        return f"{string.capwords(self.short_name)}, {self.city} {self.state}"

    @property
    def track_name(self):
        return f"{string.capwords(self.name)}"

    class META:
        unique = "name"


class Race(Base):
    name = models.CharField(max_length=64, default="NASCAR Cup Series Race at")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    race_date = models.DateField(
        null=False, default=django.utils.timezone.now, unique=True
    )
    # website = models.URLField(null=True, blank=True)
    laps = models.IntegerField(default=-1)
    # If checked load_all will reload results data and or create a default
    # results file as the race date example: 00-00-2025.csv
    reload = models.BooleanField(default=False)
    # creates a data results file in beerme2, resets after empty file has been created
    create_results_file = models.BooleanField(default=True, name="create_results_file")

    def __str__(self) -> str:
        return f"{self.name}"

    class META:
        unique_together = ("track", "race_date")
        orderby = ["-race_date"]


class Driver(Base):
    name = models.CharField(max_length=64, null=False, unique=True)
    website = models.URLField(null=True, blank=True)
    # slug = models.TextField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class RaceResult(Base):
    """One Race One Driver"""

    def __str__(self) -> str:
        return f"{self.driver} {self.finish_pos}"

    MANUFACTURER_CHOICES = {
        "Chevrolet": "CHEVROLET",
        "Ford": "FORD",
        "Toyota": "TOYOTA",
    }
    team = models.CharField(max_length=64, null=True)
    # team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # manufacturer = models.CharField(
    #     max_length=32, default="N/A", choices=MANUFACTURER_CHOICES
    # )
    manufacturer = models.CharField(max_length=64, null=True)

    start_pos = models.IntegerField(default=-1)
    finish_pos = models.IntegerField(default=-1)
    car_no = models.IntegerField(default=-1)
    laps = models.IntegerField(default=11)
    start = models.IntegerField(default=-1)
    led = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    penality = models.IntegerField(default=0)
    # From nascar the practice position
    practice_pos = models.IntegerField(default=0)
    # TODO: Fix a solution for verbose_name

    class META:
        verbose_name_plural = "Race Results"
        verbose_name = "Race Results"
        ordering = ["driver__name"]
        unique_together = ["race", "driver"]


class Bet(Base):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    finish = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.race.name} - {self.player.name} - {self.driver.name}"

    class Meta:
        unique_together = ("race", "driver")

    # constraints = [
    #     models.UniqueConstraint(
    #         fields=["race", "player", "driver"], name="unique_bet"
    #     )
    # ]


class RaceSettings(Base):
    """
    Source directory for all race results csv, .txt files are located

    Args:
        Base (_type_): _description_
    """

    source_directory = models.CharField(
        max_length=128,
        default="C:\\Users\\me\\Documents\\VisualCodeSource\\beerme2_db\\scripts\\csv_data\\",
        name="src_dir",
    )
    contents = models.CharField(default="race_results", null=False, max_length=32)

    @property
    def src_dir(self):
        return self.source_directory

    def __str__(self) -> str:
        return f"{self.src_dir}"


class ScoreBoard(Base):
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.related_name
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)
    winner = models.ForeignKey(
        Bet, on_delete=models.CASCADE, null=True, related_name="+"
    )
    looser = models.ForeignKey(
        Bet, on_delete=models.CASCADE, null=True, related_name="+"
    )

    def __str__(self) -> str:
        return f"{self.winner} ---- {self.race} "

    # @property
    # def looser(self):
    #     return self._looser

    # @looser.setter
    # def looser(self, value):
    #     self._looser = value

    # @property
    # def winner(self):
    #     return self._winner

    # @winner.setter
    # def winner(self, value):
    #     self._winner = value

    # def score_the_race(self, race: Race):
    #     for bet in Bet.objects.filter(race=race):
    #         print(f"{bet.race} - {bet.player}")

    # class META:
    #     unique = ["winner", "looser", "race"]
