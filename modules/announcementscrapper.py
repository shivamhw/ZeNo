from typing import Any
from modules import data
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import datetime
import re

# url for announcement
url = "https://www.iiita.ac.in/announcements.php?page=1"

def solve_date(extracted_date: Any) -> str:
    return re.sub(r'(\d)(st|nd|rd|th)', r'\1', extracted_date)


class AnnouncementParser:
    def __init__(self, current_announcement):
        self.current_announcement = current_announcement

    # Instance method
    def get_title(self) -> str:
        return self.current_announcement.findAll("div", {"class": "span8 announcementTitle"})[0]. \
            findAll('h3')[0].get_text()

    # Instance method
    def get_link(self) -> str:
        url = self.current_announcement.findAll("div", {"class": "span8 announcementTitle"})[0].\
            findAll('a')[0].get('href')
        parsed_url = urlparse(url, 'http')
        if parsed_url.netloc == '':
            return ('https://www.iiita.ac.in' + parsed_url.path).replace(" ", "/ ")
        else:
            return ("https://" + parsed_url.netloc + parsed_url.path).replace(" ", "/ ")

    # Instance method
    def get_content(self) -> str:
        return self.current_announcement.findAll("div", {"class": "span8 announcementContent"})[0].\
            findAll('p')[0].get_text()

    # Instance method
    def get_date(self) -> str:
        extracted_date = self.current_announcement.findAll("div", {"class": "span8 announcementDate"})[0]. \
            findAll('em')[0].get_text()
        return datetime.datetime.strptime(solve_date(extracted_date), " %d %b, %Y ").strftime('%d/%m/%Y')


def update():
    try:
        fetch_data = requests.get(url)
    except requests.exceptions.RequestException as e:
        return e
    data.AnnouncementUpdate.soup = BeautifulSoup(fetch_data.text, 'lxml')
    date_id_pair = {}
    for current_announcement in data.AnnouncementUpdate.soup.findAll("div", {"class": "span8 announcementBox"}):
        date_clean = AnnouncementParser(current_announcement).get_date()
        date_id_pair[date_clean] = current_announcement.get("id")
    data.AnnouncementUpdate.sorted_id = [i[1] for i in list(sorted(date_id_pair.items(), key=lambda t: t[1],
                                                                   reverse=True))]

