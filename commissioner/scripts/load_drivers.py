import csv
import logging
import os
import re
import select
import sys
from collections import namedtuple
from pathlib import Path

from commissioner.models import Driver, Player, RaceSettings

date_format = "%m-%d-%Y"
# the race results data source , .txt files
source_txt_race_file = (
    Path(__file__).resolve().parent.parent.parent / "commissioner" / "scripts"
)

if not os.path.isdir(source_txt_race_file):
    print(f"No Such Directory {source_txt_race_file}")
    exit()

try:
    source_txt_race_file = RaceSettings.objects.get(contents="race_results")
    source_csv_files = Path(__file__).resolve().parent.parent / "scripts" / "csv_data"
except Exception as e:
    print(f"Oh Snap! {e}")
    exit()

# logger = logging.getLogger(__name__)
try:
    logging.basicConfig(
        filename=Path(__file__).resolve().parent.parent
        / "scripts"
        / "logs"
        / "load_all.txt",
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
        return Driver.objects.get(name=row[0])

    except Driver.DoesNotExist as e:
        driver = Driver()
        # TODO: many to many insert
        driver.name = row[0]
        driver.slug = row[2]
        driver.website = row[1]
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


def load_drivers():
    logging.debug(f"Source of the data is {source_csv_files}")
    try:
        with open(f"{source_csv_files}/drivers.csv") as f:
            reader = csv.reader(f, delimiter=",")
            DriverInfo = namedtuple("DriverInfo", next(reader), rename=True)
            try:
                for row in reader:
                    data = DriverInfo(*row)
                    driver = look_up_driver(data)
            except Exception as e:
                print(row)
                sys.exit(f"load_drivers {reader.line_num} {e}")

    except Exception as e:
        print(f"load_drivers() -> {e}")
        exit()


def run():
    logging.info("Starting to Load Drivers")
    load_drivers()
    load_players()
    print("Runscript OK")
