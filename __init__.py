from dotenv import load_dotenv
import telebot
import logging

users_dict = {}
poll_dict = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('zeno.log')
formatter = logging.Formatter('%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
load_dotenv("config.env")
TELE = '1420627782:AAHOEG9qjDK-4qOEGJg7YFnWnp8ieIS6iD4'
bot = telebot.TeleBot(TELE) or None
