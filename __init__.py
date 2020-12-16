from dotenv import load_dotenv
import telebot
from modules import dbhelper
users_dict = {}
poll_dict = {}

load_dotenv("config.env")
TELE = '1420627782:AAHOEG9qjDK-4qOEGJg7YFnWnp8ieIS6iD4'
bot = telebot.TeleBot(TELE) or None
DB = dbhelper.Dbhelper()
