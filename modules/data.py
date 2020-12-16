from dataclasses import dataclass
from typing import List
from modules import announcementscrapper


@dataclass
class CurrentAnnouncement:
    date: str = ""
    title: str = ""
    content: str = ""
    link: str = ""


@dataclass
class AnnouncementUpdate:
    sorted_id: List[int]
    soup: str = ""
    update_id: int = 0


class PollData:
    def __init__(self):
        self.id = 0
        self.active_polls = None
        self.active_poll_count = None
        self.question = None  # poll question corresponding to each poll id
        self.options = None
        self.response = None
        self.about_poll = None  # stores the data why this poll is conducted


class User:
    def __init__(self, username):
        self.name = None
        self.username = username
        self.password = None
        self.jwt_token = None
        self.cookie = None
        self.cs_token = None
        self.request_no = 0
        self.is_admin = False
        self.current_poll = None
        self.answered_poll = None  # stores the object of all polls answered by user

    def get_announcement(self) -> dict:
        if self.request_no == 5:
            self.request_no = 0
        if AnnouncementUpdate.soup == "":
            announcementscrapper.update()
        for anc in AnnouncementUpdate.soup.findAll("div", {"class": "span8 announcementBox"}):
            if anc.get("id") == AnnouncementUpdate.sorted_id[self.request_no]:
                self.request_no += 1
                current_announcement = announcementscrapper.AnnouncementParser(anc)
                return {"date": current_announcement.get_date(), "title": current_announcement.get_title(),
                        "content": current_announcement.get_content(), "link": current_announcement.get_link()}
