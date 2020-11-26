from modules import aviralscrapper as avi
from modules.helper import Parser
from modules import classlinks, admin
# from helper import Parser
from modules.data import User
from modules import dbhelper
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
    markup.add(InlineKeyboardButton("Online Class links", callback_data="classlinks"))
    if(user.is_admin):
        bot.send_message(message.chat.id, "Awesome you are an admin!!!")
        markup.add(InlineKeyboardButton("Admin Panel", callback_data="admin_panel"))
    bot.send_message(message.chat.id, "Here are some things you can do", reply_markup=markup)

### admin panel
def admin_panel(user, message):
    bot.send_message(message.chat.id, "Admins have superpowers!!! Use it wisely.")
    markup = InlineKeyboardMarkup()
    for i, j in admin.get_modules().items():
        markup.add(InlineKeyboardButton(j, callback_data=i))
    bot.send_message(message.chat.id, "Here are some things only admin can do", reply_markup=markup)

# def new_page(user, message):
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 1
#     markup.add(InlineKeyboardButton("Aviral marks", callback_data="aviral"),
#                                     InlineKeyboardButton("New announcements", callback_data="announcement"),
#                                     InlineKeyboardButton("Refresh announcements", callback_data="refresh_anc"))
#     bot.send_message(message.chat.id, "Here are some things you can do", reply_markup=markup)

def get_announcement(message, user):
    anc = user.get_announcement()
    output_string = "Announcement No: "+str(user.request_no) + '\n'
    output_string += "\n Date:-" + str(anc['date'])
    output_string += "\n Title:-" + str(anc['title'])
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(text="Notification Link", url=str(anc['link'])), InlineKeyboardButton(text="Next ->", callback_data="announcement"))
    bot.send_message(message.chat.id, output_string, reply_markup=markup)


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
    elif call.data == "classlinks":
        bot.answer_callback_query(call.id)
        user = users_dict[call.message.chat.id]
        user.request_no = 0
        if(call.message.chat.id in users_dict):
            get_classlinks(call.message, users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Please /start again")
    elif call.data == "admin_panel":
        bot.answer_callback_query(call.id)
        user = users_dict[call.message.chat.id]
        admin_panel(user, call.message)
    elif call.data in admin.get_modules():
        bot.answer_callback_query(call.id)
        if(call.message.chat.id in users_dict):
            admin.handle(bot, users_dict, call.message, call.data)
        else:
            bot.send_message(call.message.chat.id, "Please /start again")
    elif call.data == "sure_a":
        bot.answer_callback_query(call.id)
        admin.broadcast(bot, users_dict)


#### Handler functions

def get_marks(message, user):
    marks = Parser.marks_parser(avi.get_marks(user))
    bot.send_message(message.chat.id, marks)

def get_classlinks(message, user):
    raw = classlinks.get_links(user)
    for i,j in raw.items():
        markup = InlineKeyboardMarkup()
        markup.row_width = len(j)
        markup.add(InlineKeyboardButton("Link", url=j[0]))
        bot.send_message(message.chat.id, i , reply_markup=markup)


##Helper functions


def trial_setup(user):
    admins = ['mit2020122', 'mit2020080']
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

def is_reg(message):
    if(message.chat.id in users_dict):
        return True
    db = Dbhelper()
    if(db.is_registered(message.chat.id)):  ## to be done by nikhil
    username, password = db.get_session(message.chat.id)
    user = User(username)
    user.password = password
    if(avi.login(user)):
    bot.send_message(message.chat.id, "from db")
         return True
    else:
         bot.send_message(message.chat.id, "error from db side please /start again")
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
