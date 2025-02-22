import csv
import logging
import os
import re
import select
import sys
from collections import namedtuple
from pathlib import Path

from commissioner.models import Driver, Player, RaceResult, RaceSettings

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


def look_up_driver(row):
    try:
        return Driver.objects.get(name=row.DRIVER)

    except Driver.DoesNotExist as e:
        driver = Driver()
        # TODO: many to many insert
        driver.name = row.DRIVER
        driver.slug = ""
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
    if not os.path.isfile(filename):
        with open(filename, "w"):
            pass
        print(f"Created results file {filename}, load the data... exiting")
        exit()


def load_race_results(race_date):
    results_csv_filename = f"{source_csv_directory}\\{race_date}.csv"
    logging.debug(f"Source of the data is {results_csv_filename}")
    check_for_results_file(results_csv_filename)
    try:
        with open(f"{source_csv_directory}\\{race_date}.csv") as f:
            reader = csv.reader(f, delimiter="\t")
            RaceResultsInfo = namedtuple("RaceResultsInfo", next(reader), rename=True)
            try:
                for row in reader:
                    data = RaceResultsInfo(*row)
                    look_up_driver(data)
            except Exception as e:
                print(row)
                sys.exit(f"load_race_results {reader.line_num} {e}")

    except Exception as e:
        print(f"load_race_results() -> {e}")
        exit()


def run():
    logging.info("Starting to Load Race Results")
    # need to prompt for the date
    load_race_results("02-16-2025")
    print("Runscript OK")
