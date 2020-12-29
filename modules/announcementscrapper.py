from typing import Any
from ZeNo import bot, users_dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from modules import data
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import datetime
import re

# url for announcement
url = "https://www.iiita.ac.in/announcements.php?page=1"


# @bot.callback_query_handler(func=lambda call: call.data in ["announcement", "refresh_anc"])
def announce_callback_handler(call):
    if call.data == "announcement":
        bot.answer_callback_query(call.id)
        if call.message.chat.id in users_dict:
            get_announcement(call.message, users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Please /start again")
    elif call.data == "refresh_anc":
        bot.answer_callback_query(call.id)
        user = users_dict[call.message.chat.id]
        user.request_no = 0
        if call.message.chat.id in users_dict:
            get_announcement(call.message, users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Please /start again")


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
        url_1 = self.current_announcement.findAll("div", {"class": "span8 announcementTitle"})[0].\
            findAll('a')[0].get('href')
        parsed_url = urlparse(url_1, 'http')
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


def get_announcement(message, user):
    anc = user.get_announcement()
    output_string = "Announcement No: "+str(user.request_no) + '\n'
    output_string += "\n Date:-" + str(anc['date'])
    output_string += "\n Title:-" + str(anc['title'])
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(text="Notification Link", url=str(anc['link'])),
               InlineKeyboardButton(text="Next ->", callback_data="announcement"))
    bot.send_message(message.chat.id, output_string, reply_markup=markup)
