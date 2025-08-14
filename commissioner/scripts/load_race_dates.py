from pathlib import Path

import requests
from bs4 import BeautifulSoup

HOST = "https://www.espn.com/racing/results/_/year/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
TARGET_RESULTS = r"C:\Users\me\Documents\VisualCodeSource\beerme2_db\commissioner\scripts\race_date_data"


def bs(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        print(response.status_code)
        return soup
    else:
        print(f"Failed to retrieve data from {url}")
        return None


class RaceDate:
    def __init__(self, year):
        self.year = year
        print(f"Processing year: {year}")
        self.url = f"{HOST}{year}"
        self.soup = bs(self.url)

    def get_year_schedule(self):
        # https://www.geeksforgeeks.org/python/extract-all-the-urls-from-the-webpage-using-python/
        urls = []
        year = ""
        if self.soup:
            urls.extend(
                link.get("href")
                for link in self.soup.find_all("a")
                if link.get("href").__contains__("/racing/raceresults/")
            )
        # Filter out URLs that do not match the expected pattern
        print(f"Processing URL: {self.url.split('/')[-1]}")
        id = self.url.split("/")[-1]
        year = id[0:4]
        month = id[4:6]
        day = id[6:8]
        print(f"year={year} month={month} day={day}")
        output_file_name = f"{TARGET_RESULTS}/{month}-{day}-{year}.csv"
        my_file = Path(output_file_name)
        if my_file.is_file():
            # file exists
            print(f"{my_file} exists {Path(output_file_name).stat().st_size} bytes")
            return

    # hot_soup = bs(url)
    # cnt = 0
    # if hot_soup:
    #         f = open(output_file_name, "w")
    #         if table_rows := hot_soup.find_all("tr"):
    #         for tr in table_rows:
    #                 for data_cell in tr.find_all("td"):
    #                 if cnt == 0:
    #                         cnt = 1
    #                         continue
    #                         # print(child)
    #                 cnt += 1
    #                 # print(data_cell.get_text(strip=True), end="\t")
    #                 f.write(data_cell.get_text(strip=True) + "\t")
    #                 if cnt > 1:
    #                 f.write("\n")
    # else:
    # print(f"End of {year} results.")

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


def run():
    for year in range(2000, 2001):
        x = RaceDate(year)
        x.get_year_schedule()
