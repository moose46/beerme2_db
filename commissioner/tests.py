from os import name

from django.contrib.auth.models import User
from django.test import TestCase, tag

# Create your tests here.
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

"""
     python manage.py test
"""


# https://docs.djangoproject.com/en/5.1/topics/testing/advanced/
class StateTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="admin", password="admin")
        user = User.objects.get(username="admin")
        State.objects.create(name="Ohio", user_id=user.pk)
        Track.objects.create(name="Daytona", user_id=user.pk)
        Race.objects.create(name="Daytona 500", user_id=user.pk)
        # add team
        Team.objects.create(name="Penske", user_id=user.pk)
        # Add drivers
        team = Team.objects.get(name="Penske")
        Driver.objects.create(name="Ricky Rudd", user_id=user.pk, team=team)
        Driver.objects.create(name="Ryan Blaney", user_id=user.pk, team=team)

        # Add Players
        Player.objects.create(name="Greg", user_id=user.pk)
        Player.objects.create(name="Bob", user_id=user.pk)

        # Add Track
        self.daytona = Track.objects.get(name="Daytona")

        # Add race
        self.daytona_500_race = Race.objects.get(name="Daytona 500")

        # Add Drivers
        self.ricky = Driver.objects.get(name="Ricky Rudd")
        self.blaney = Driver.objects.get(name="Ryan Blaney")

        # Add State
        self.state = State.objects.get(name="Ohio")

        # Add Players
        self.player_greg = Player.objects.get(name="Greg")
        self.player_bob = Player.objects.get(name="Bob")

        # Add Bets
        Bet.objects.create(
            player=self.player_greg,
            driver=self.blaney,
            race=self.daytona_500_race,
            user_id=user.pk,
        )
        Bet.objects.create(
            player=self.player_bob,
            driver=self.ricky,
            race=self.daytona_500_race,
            user_id=user.pk,
        )
        # Add Race Results
        RaceResult.objects.create(
            driver=self.ricky,
            team="Rudd Racing",
            race=self.daytona_500_race,
            finish_pos=1,
            user_id=user.pk,
        )

    # https://docs.djangoproject.com/en/5.1/topics/testing/tools/
    @tag("state")
    def test_state(self):
        self.assertEqual(self.state.state_name, "Ohio")
        self.assertIsNotNone(self.state.createdAt)

    @tag("track")
    def test_track(self):
        self.assertEqual(self.daytona.name, "Daytona")

    @tag("race")
    def test_race(self):
        self.assertEqual(self.daytona_500_race.name, "Daytona 500")

    @tag("driver")
    def test_driver(self):
        ricky = Driver.objects.get(name="Ricky Rudd")
        self.assertEqual(ricky.name, "Ricky Rudd")

    def test_race_results(self):
        results = RaceResult.objects.get(finish_pos=1)
        self.assertEqual(results.driver.name, "Ricky Rudd")

    def test_bet(self):
        bob = Bet.objects.get(player=self.player_bob)
        greg = Bet.objects.get(player=self.player_greg)
        self.assertEqual(bob.driver.name, self.ricky.name)
