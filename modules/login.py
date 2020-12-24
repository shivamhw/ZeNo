from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from ZeNo import users_dict, bot
from modules.data import User
from modules import aviralscrapper as avi
from modules.dbhelper import is_in_db
@bot.callback_query_handler(func=lambda call: call.data == "main_login")
def login_callback(call):
    if call.message.chat.id not in users_dict and not is_in_db(call.message.chat.id):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Please enter you Roll number like mitXXXXXXXXX")
        bot.register_next_step_handler(call.message, get_username)
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "You are already logged in just click /start")


def get_username(message):
    username = message.text.lower()
    # user = User(username)
    # users_dict[message.chat.id] = user
    bot.reply_to(message, "please enter you login pass")
    bot.register_next_step_handler(message, get_password, username)


def get_password(message, username):
    password = message.text
    # user = users_dict[message.chat.id]
    # user.password = password
    user = avi.login(username, password, message.chat.id)
    if user is None:
        bot.send_message(message.chat.id, "sahi dal le waps se.... Waps start kro /start")
        # del users_dict[message.chat.id]
    else:
        users_dict[message.chat.id] = user
        # trial_setup(user)
        front_page(user, message)


def front_page(user, message):
    bot.send_message(message.chat.id, "Hiii " + user.name + " ... ")
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Aviral marks", callback_data="aviral"),
               InlineKeyboardButton("New announcements", callback_data="announcement"))
    markup.add(InlineKeyboardButton("Online Class links", callback_data="classlinks"))
    markup.add(InlineKeyboardButton("Create Poll", callback_data="create_poll"),
               InlineKeyboardButton("Show Active Poll", callback_data="show_poll"))
    if user.is_admin:
        bot.send_message(message.chat.id, "Awesome you are an admin!!!")
        markup.add(InlineKeyboardButton("Admin Panel", callback_data="admin_panel"))
    bot.send_message(message.chat.id, "Here are some things you can do", reply_markup=markup)


# def trial_setup(user):
#     admins = ['mit2020122', 'mit2020080']
#     if user.username in admins:
#         user.is_admin = True
