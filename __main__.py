from modules import admin, classlinks, polls
from ZeNo import bot, users_dict, poll_dict
from modules.login import front_page
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.dbhelper import is_in_db, get_user_db
import time
import os
import subprocess

def gen_markup_login():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Login Now", callback_data="main_login"),
                               InlineKeyboardButton("No Thanks", callback_data="cancel"))
    markup.row_width = 2
    markup.add(
               InlineKeyboardButton("About", callback_data="about"),
               InlineKeyboardButton("FAQ", callback_data="faq"))
    return markup

def is_reg(message):
    if(message.chat.id in users_dict):
        return True
    elif(is_in_db(message.chat.id)):
        bot.send_message(message.chat.id, "not in cache but trying to get it from db....")
        user = get_user_db(message.chat.id)
        users_dict[message.chat.id] = user
        return True
    return False

### Handlers
@bot.message_handler(commands=['start'])
def message_handler(message):
    hello_msg = ("Hey, I am ZeNo. I was created to save your time so you can do your assignments with one hand!\n"
				 "Please wait while i check your status.....")
    bot.send_message(message.chat.id, hello_msg)
    if(is_reg(message)):
        bot.send_message(message.chat.id, "you are registered with us!")
        front_page(users_dict[message.chat.id], message)
    else:
        bot.send_message(message.chat.id, "ohhh! you are not registered with us.\nWant to login??", reply_markup=gen_markup_login())

@bot.message_handler(commands=['hi'])
def message_handler(message):
    if(is_reg(message)):
        front_page(users_dict[message.chat.id], message)
    else:
        bot.send_message(message.chat.id, "ohhh! you are not registered with us.\nWant to login??", reply_markup=gen_markup_login())


#### BOT STARTING POINT

try:
    time.sleep(2)
    bot.polling(none_stop=True)
except:
    subprocess.call(['bash', './reset.sh', os.getcwnd()])
