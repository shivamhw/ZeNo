import os
import telebot
from pymongo import MongoClient


# MongoURI = "mongodb+srv://shivamhw:katOLMpqLaK2EqI3@cluster0.vuse2.mongodb.net/ZeNo?retryWrites=true&w=majority"
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
