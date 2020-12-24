import os
import telebot
from modules import dbhelper
users_dict = {}
poll_dict = {}

TELE = os.environ['TELE']
bot = telebot.TeleBot(TELE) or None
if bot is None:
    print("error in getting token")
    exit(1)
DB = dbhelper.Dbhelper()
