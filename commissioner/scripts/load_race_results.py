import csv
import logging
import os
import re
import select
import sys
from collections import namedtuple
from pathlib import Path

from django.forms import NullBooleanField

from commissioner.models import (
    Bet,
    Driver,
    Player,
    Race,
    RaceResult,
    RaceSettings,
    ScoreBoard,
)

date_format = "%m-%d-%Y"
# the race results data source , .txt files
source_txt_race_file = (
    Path(__file__).resolve().parent.parent.parent / "commissioner" / "scripts"
)

if not os.path.isdir(source_txt_race_file):
    print(f"No Such Directory {source_txt_race_file}")
    exit()

try:
    source_csv_directory = (
        Path(__file__).resolve().parent.parent / "scripts" / "csv_data"
    )
    source_data_directory = Path("..") / "beerme2" / "data"
except Exception as e:
    print(f"Oh Snap! {e}")
    exit()

# logger = logging.getLogger(__name__)
try:
    logging.basicConfig(
        filename=Path(__file__).resolve().parent.parent
        / "scripts"
        / "logs"
        / "load_race_results.txt",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w",
    )
except Exception as e:
    print(f"{e}")
    exit()

from datetime import datetime


def is_valid_date(date_str):
    # Checks if a date string is valid ISO 8601 format
    # Returns True if valid, False otherwise
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False

def lookup_driver_team(driver):
    pass
def look_up_driver(row):
    try:
        return Driver.objects.get(name=row.DRIVER)

    except Driver.DoesNotExist as e:
        driver = Driver()
        # TODO: many to many insert
        driver.name = row.DRIVER
        # driver.slug = ""
        driver.website = ""
        driver.save()
        logging.debug(f"Created {driver.name}")
        return driver


def load_players():
    try:
        Player.objects.create(name="Bob")
        Player.objects.create(name="Greg")
    except Exception as e:
        print(f"{e}")
        exit()

def check_for_results_file(filename):
    head_tail = os.path.split(filename)
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            f.write("\n")
        print(f"Created results file {head_tail[1]}, check_for_results_file()")
        # exit()


from dateutil.parser import parse


def CheckRaceRecord(race_date):
    """
    This function queries the Race model to determine if any race records
    exist for the specified race_date.

    Args:
        race_date: The date of the race to check for.

    Returns:
        True if a race record exists for the given date, False otherwise.
    """
    dt = parse(race_date)
    race_date = dt.strftime("%Y-%m-%d")
    logging.info(f"Check Race Date {race_date}")
    return Race.objects.filter(race_date=race_date).exists()


def insert_race_results(driver: Driver, data, race):
    # If this race has already been loaded return
    if not Race.create_results_file:
        return
    finish = RaceResult()

    finish.finish_pos = data.POS
    finish.start_pos = data.START
    finish.race = race
    finish.race_id = race.id
    finish.track_id = race.track_id
    finish.driver = driver
    finish.car_no = data.CAR
    finish.manufacturer = data.MANUFACTURER
    finish.laps = data.LAPS
    finish.led = data.LED
    finish.save()


def load_race_results(race):
    # convert the race_date to a string
    race_date = race.race_date.strftime("%m-%d-%Y")
    if not CheckRaceRecord(race_date=race_date):
        print(
            f"Race data is not entered yet, enter the race record for {race_date} first!"
        )
        logging.warning(
            f"Race data is not entered yet, enter the race record for {race_date} first!"
        )
        exit(-1)
    results_csv_filename = f"{source_csv_directory}\\{race_date}.csv"
    # results_data_filename = f"{source_data_directory}\\{race_date}.csv"
    logging.debug(f"Source of the data is {results_csv_filename}")
    # logging.debug(f"Source of the data (beerme2) is {results_data_filename}")
    check_for_results_file(results_csv_filename)
    # Check beerme2 for the result file also
    # check_for_results_file(results_data_filename)
    try:
        with open(f"{source_csv_directory}\\{race_date}.csv") as f:
            reader = csv.reader(f, delimiter="\t")
            RaceResultsInfo = namedtuple("RaceResultsInfo", next(reader), rename=True)
            try:
                row_count = 0
                for row in reader:
                    data = RaceResultsInfo(*row)
                    row_count += 1
                    driver = look_up_driver(data)
                    insert_race_results(driver, data, race)
                # if there is no data in the csv file, exit
                if row_count == 0:
                    logging.warning("No Results in the data file ...")
                    return False
                else:
                    print(f"Loading {race_date}")
            except Exception as e:
                print(row)
                sys.exit(f"load_race_results {e}")

    except Exception as e1:
        print(f"load_race_results() -> {e1}")
        exit()
    return True


def update_bets(race):
    try:
        for bet in Bet.objects.filter(race=race):
            race_driver_results = (
                RaceResult.objects.filter(driver=bet.driver)
                .filter(race=bet.race)
                .order_by("finish_pos")
            )
            print(f"{bet.player} {bet.race} {race_driver_results[0].finish_pos}")
            bet.finish = race_driver_results[0].finish_pos
            bet.save()
    except Exception as e:
        print(f"UPDATE_BETS - {e} {bet.player} {bet.race}")
        exit(-1)


from django.db.models import Q

bet_results_list = []


def score_the_race(race: Race):
    # bets = Bet.objects.filter(race_id=race)
    # if No bets made on this race, return
    # if bets.count() == 0:
    #     return
    # print(f"bets={bets}")
    # print(f"{race}")
    # clear the score board
    sb = ScoreBoard.objects.filter().delete()
    bet_cnt = 0
    # returns all bets for one race
    try:
        rawsql = RaceResult.objects.raw(
            "SELECT BET.ID, FINISH_POS, BET.RACE_ID, BET.PLAYER_ID FROM COMMISSIONER_RACERESULT RACERESULTS, COMMISSIONER_BET BET WHERE	BET.DRIVER_ID = RACERESULTS.DRIVER_ID AND BET.RACE_ID = RACERESULTS.RACE_ID	AND FINISH_POS = (SELECT MIN(FINISH_POS) FROM COMMISSIONER_RACERESULT R, COMMISSIONER_BET B WHERE B.RACE_ID = R.RACE_ID	AND R.DRIVER_ID = B.DRIVER_ID AND RACERESULTS.RACE_ID = B.RACE_ID	) GROUP BY	1,	2,	3, 4"
        )
        for r in rawsql:
            # print(f" --- {r.id} {r.finish_pos} {r.race_id} {r.player_id}")
            sb = ScoreBoard()
            sb.race = Race.objects.get(pk=r.race_id)
            sb.winner = Bet.objects.get(pk=r.player_id)
            sb.beers = 2 if r.finish_pos == 1 else 1
            sb.save()
    except Exception as e:
        print(f"{e}")
        exit()
    # for b in bets:

    #     try:
    #         # get the results for each bet
    #         results = RaceResult.objects.filter(
    #             race_id=race,
    #             driver_id=b.driver,
    #             # Q(race_id=b.race) & Q(driver_id=b.driver)
    #         )
    #     except Exception as e:
    #         print(
    #             f"{e}  --Info-- bet_race.pk={b.race.pk} race_pk={race.pk} driver_id={b.driver.id}"
    #         )
    #         exit()


def run():
    logging.info("Starting to Load Race Results")
    # need to prompt for the date
    for race in Race.objects.all():
        # Create results file is checked
        if race.create_results_file == True:
            try:
                # remove all data from this race and refresh the data
                RaceResult.objects.filter(race_id=race.pk).delete()
            except Exception as e:
                print(f"{e} {race}")
                exit()
            if load_race_results(race):
                # mark the race results as loaded
                race.create_results_file = False
                race.save()
        update_bets(race)
        sb = ScoreBoard()
        score_the_race(race)
    print("Runscript OK")
