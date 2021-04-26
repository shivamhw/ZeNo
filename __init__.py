import os
import telebot
from pymongo import MongoClient
from importlib import import_module
from modules import ALL_MODULES

users_dict = {}
poll_dict = {}



TELE = os.environ['TELE']
MongoURI = os.environ['MongoURI']
bot = telebot.TeleBot(TELE) or None
if bot is None:
    print("error in getting token")
    exit(1)

client = MongoClient(MongoURI)
MONGO = client.zeno

for module_name in ALL_MODULES:
    imported_module = import_module("ZeNo.modules." + module_name)
