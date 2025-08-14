import re
import urllib.request
from pathlib import Path
from pprint import pprint
from urllib import response

import requests
from bs4 import BeautifulSoup
from html_table_parser.parser import HTMLTableParser

TARGET_RESULTS = (
    r"C:\Users\me\Documents\VisualCodeSource\beerme2_db\commissioner\scripts\csv_data"
)
HOST = "https://www.espn.com/racing/raceresults/_/series/sprint/raceId/202404280004"
HOST = "https://www.espn.com/racing/results/_/year/"
# HOST = "https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI"
PORT = 80
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def bs(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        print(response.status_code)
        return soup
    else:
        print(f"Failed to retrieve data from {url}")
        return None


def process_results(soup):
    # https://www.geeksforgeeks.org/python/extract-all-the-urls-from-the-webpage-using-python/
    urls = []
    year = ""
    if soup:
        urls.extend(
            link.get("href")
            for link in soup.find_all("a")
            if link.get("href").__contains__("/racing/raceresults/")
        )
    for url in urls:
        # Filter out URLs that do not match the expected pattern
        print(f"Processing URL: {url.split('/')[-1]}")
        id = url.split("/")[-1]
        year = id[0:4]
        month = id[4:6]
        day = id[6:8]
        print(f"year={year} month={month} day={day}")
        output_file_name = f"{TARGET_RESULTS}/{month}-{day}-{year}.csv"
        my_file = Path(output_file_name)
        if my_file.is_file():
            # file exists
            print(f"{my_file} exists {Path(output_file_name).stat().st_size} bytes")

            continue
        hot_soup = bs(url)
        cnt = 0
        if hot_soup:
            f = open(output_file_name, "w")
            if table_rows := hot_soup.find_all("tr"):
                for tr in table_rows:
                    for data_cell in tr.find_all("td"):
                        if cnt == 0:
                            cnt = 1
                            continue
                            # print(child)
                        cnt += 1
                        # print(data_cell.get_text(strip=True), end="\t")
                        f.write(data_cell.get_text(strip=True) + "\t")
                    if cnt > 1:
                        f.write("\n")
    else:
        print(f"End of {year} results.")


def run():
    for year in range(1980, 2000):
        print(f"Processing year: {year}")
        url = f"{HOST}{year}"
        soup = bs(url)
        if soup:
            process_results(soup)
        else:
            print(f"No data found for year {year}")
