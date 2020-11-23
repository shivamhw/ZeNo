from modules import aviralscrapper as avi
from modules.helper import Parser
# from helper import Parser
from modules.data import User
from dotenv import load_dotenv
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv("config.env")
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN")) or None
users_dict = {}





#### Front page for loggedin User
def front_page(user, message):
    bot.send_message(message.chat.id, "Hiii "+user.name+" ... ")
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Aviral marks", callback_data="aviral"),
                                    InlineKeyboardButton("New announcements", callback_data="announcement"))
    if(user.is_admin):
        markup.add(InlineKeyboardButton("Admin Panel", callback_data="admin_panel"))
    bot.send_message(message.chat.id, "Here are some things you can do", reply_markup=markup)


def new_page(user, message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Aviral marks", callback_data="aviral"),
                                    InlineKeyboardButton("New announcements", callback_data="announcement"),
                                    InlineKeyboardButton("Refresh annocements", callback_data="refresh_anc"))
    bot.send_message(message.chat.id, "Here are some things you can do", reply_markup=markup)

def get_announcement(message, user):
    anc = user.get_announcement()
    output_string = "Announcement No: "+str(user.request_no)
    output_string += "\n Date:-" + str(anc['date'])
    output_string += "\n Title:-" + str(anc['title'])
    output_string += "\n Content:-" + str(anc['content'])
    #markup = InlineKeyboardMarkup()
    #markup.row_width = 1
    bot.send_message(message.chat.id, output_string)
    # markup.add(InlineKeyboardButton(text = "Notification Link", url = str(anc['link'])))
    new_page(user, message)


# main button event handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "main_login":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id , "Please enter you Roll number like mitXXXXXXXXX")
        bot.register_next_step_handler(call.message, get_username)
    elif call.data == "aviral":
        bot.answer_callback_query(call.id)
        if (call.message.chat.id in users_dict):
            get_marks(call.message, users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id ,"Please /start again")
    elif call.data == "announcement":
        bot.answer_callback_query(call.id)
        if (call.message.chat.id in users_dict):
            get_announcement(call.message, users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Please /start again")
    elif call.data == "refresh_anc":
        bot.answer_callback_query(call.id)
        user = users_dict[call.message.chat.id]
        user.request_no = 0
        if(call.message.chat.id in users_dict):
            get_announcement(call.message, users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Please /start again")


#### Handler functions

def get_marks(message, user):
    marks = Parser.marks_parser(avi.get_marks(user))
    bot.send_message(message.chat.id, marks)




##Helper functions

def trial_setup(user):
    admins = ['mit2020122']
    if(user.username in admins):
        user.is_admin = True

def get_username(message):
    username = message.text
    user = User(username)
    users_dict[message.chat.id] = user
    bot.reply_to(message, "please enter you login pass")
    bot.register_next_step_handler(message, get_password)

def get_password(message):
    password = message.text
    user = users_dict[message.chat.id]
    user.password = password
    if(not avi.login(user)):
        bot.send_message(message.chat.id, "sahi dal le waps se.... Waps start kro /start")
        del users_dict[message.chat.id]
    else:
        trial_setup(user)
        front_page(user, message)

def gen_markup_login():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Login Now", callback_data="main_login"),
                               InlineKeyboardButton("No Thanks", callback_data="cancel"))
    return markup



### Handlers
@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    hello_msg = ("Hey, I am ZeNo. I was created to save your time so you can do your assignments with one hand!\n"
				 "Please wait while i check your status.....")
    bot.send_message(message.chat.id, hello_msg)
    if(message.chat.id in users_dict):
        bot.send_message(message.chat.id, "you are registered with us!")
        front_page(users_dict[message.chat.id], message)
    else:
        bot.send_message(message.chat.id, "ohhh! you are not registered with us.\nWant to login??", reply_markup=gen_markup_login())


#### BOT STARTING POINT
bot.polling(none_stop=True)
