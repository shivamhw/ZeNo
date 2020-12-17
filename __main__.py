from modules import admin, classlinks, polls
from ZeNo import bot, users_dict, poll_dict
from modules.login import front_page
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_markup_login():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Login Now", callback_data="main_login"),
                               InlineKeyboardButton("No Thanks", callback_data="cancel"))
    return markup

def is_reg(message):
    if(message.chat.id in users_dict):
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
bot.polling(none_stop=True)
