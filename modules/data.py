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
    update_id : int = 0

class User:
    def __init__(self, username):
        self.name = None
        self.username = username
        self.password = None
        self.jwt_token = None
        self.cookie = None
        self.cs_token = None
        self.request_no = 0

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


