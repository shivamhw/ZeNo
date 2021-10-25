from ZeNo import bot, users_dict, poll_dict
from ZeNo.modules.login import front_page
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ZeNo.modules.helper import is_reg
import time

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


### Command Handlers
@bot.message_handler(commands=['start'])
def message_handler(message):
    hello_msg = ("Hey, I am ZeNo. I was created to save your time so you can do your assignments with one hand!\n"
				 "Please wait while i check your status.....")
    bot.send_message(message.chat.id, hello_msg)
    if(is_reg(message)):
        bot.send_message(message.chat.id, "you are registered with us!")
        front_page(users_dict[message.chat.id], message)
    else:
        bot.send_message(message.chat.id1, "ohhh! you are not logged in!", reply_markup=gen_markup_login())

@bot.message_handler(commands=['hi'])
def message_handler(message):
    if(is_reg(message)):
        front_page(users_dict[message.chat.id], message)
    else:
        bot.send_message(message.chat.id, "ohhh! you are not logged in!", reply_markup=gen_markup_login())





#### BOT STARTING POINT

try:
    time.sleep(2)
    bot.polling(none_stop=True)
except Exception as e:
    print(str(e))
