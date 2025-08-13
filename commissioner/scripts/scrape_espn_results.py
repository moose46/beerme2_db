from pathlib import Path
import re
import urllib.request
from pprint import pprint
from urllib import response

import requests
from bs4 import BeautifulSoup
from html_table_parser.parser import HTMLTableParser

HOST = "https://www.espn.com/racing/raceresults/_/series/sprint/raceId/202404280004"
HOST = "https://www.espn.com/racing/results/_/year/2024"
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


def run():
    soup = bs(HOST)
    # https://www.geeksforgeeks.org/python/extract-all-the-urls-from-the-webpage-using-python/
    urls = []
    if soup:
        urls.extend(
            link.get("href")
            for link in soup.find_all("a")
            if link.get("href").__contains__("/racing/raceresults/")
        )
    for url in urls:
        # Filter out URLs that do not match the expected pattern
        print(f"Processing URL: {url.split('/')[-1]}")
        id = url.split('/')[-1]
        year = id[0:4]
        month = id[4:6]
        day = id[6:8]
        print(f'year={year} month={month} day={day}')
        output_file_name = f"{month}-{day}-{year}.csv"
        hot_soup = bs(url)
        cnt = 0
        if hot_soup:
            my_file = Path(output_file_name)
            if my_file.is_file():
                # file exists
                print(f"{my_file} exists")
                continue
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
        print("Failed to parse the page.")
