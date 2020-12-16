from dotenv import load_dotenv
import telebot
from modules import dbhelper
users_dict = {}
poll_dict = {}

load_dotenv("config.env")
TELE = '1446035026:AAHCg486X5kSSgy-xrX3GPtYFR2wU4l7EGI'
bot = telebot.TeleBot(TELE) or None
DB = dbhelper.Dbhelper()