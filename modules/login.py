from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from ZeNo import users_dict, bot
from modules.helper import is_reg
from modules import aviralscrapper as avi
from modules.helper import emojis

@bot.callback_query_handler(func=lambda call: call.data == "main_login")
def login_callback(call):
    if not is_reg(call.message):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Please enter you Roll number like mitXXXXXXXXX")
        bot.register_next_step_handler(call.message, get_username)
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "You are already logged in just click /start")


@bot.callback_query_handler(func=lambda call: call.data == "logout")
def login_callback(call):
    bot.answer_callback_query(call.id)
    if not is_reg(call.message):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "you are not even logged in dada.\n Please click /start")
    else:
        bot.answer_callback_query(call.id)
        if call.message.chat.id in users_dict:
            logout(users_dict[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Sorry!! we messed up .. :(\n just click /start")


def get_username(message):
    username = message.text.lower()
    bot.reply_to(message, "please enter you login pass")
    bot.register_next_step_handler(message, get_password, username)


def get_password(message, username):
    password = message.text
    print("Login to aviral called")
    user = avi.login(username, password, message.chat.id)
    if user is None:
        bot.send_message(message.chat.id, "Can't login to aviral. please /start again")
    else:
        users_dict[message.chat.id] = user
        front_page(user, message)


def front_page(user, message):
    bot.send_message(message.chat.id, "Hiii " + user.name + " ... ")
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    # markup.add(InlineKeyboardButton("MTECH Specialization Results !", callback_data="aviral_spl"))
    markup.add(InlineKeyboardButton("Aviral marks "+emojis.get_emoji("bar_chart"),
                                    callback_data="aviral"))  # InlineKeyboardButton("New announcements", callback_data="announcement")
    markup.add(InlineKeyboardButton("Online Class links", callback_data="classlinks"))
    markup.add(InlineKeyboardButton("Logout",
                                    callback_data="logout"))  # InlineKeyboardButton("Create Poll", callback_data="create_poll"),
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("FAQ", callback_data="faq"))
    if user.is_admin:
        bot.send_message(message.chat.id, "Awesome you are an admin!!!")
        markup.add(InlineKeyboardButton("Admin Panel", callback_data="admin_panel"))
    bot.send_message(message.chat.id, "Here are some things you can do", reply_markup=markup)


def logout(user):
    try:
        user.del_user_db()
        bot.send_message(user.chat_id,
                         "Ohhhh okay then byeee....\n\nNote: After logout all your data will be deleted from our DB and cache.\n Send /hi or /start again to start")
        del users_dict[user.chat_id]
    except:
        print("Issue deleting user!!")
        bot.send_message(user.chat_id, "Error while logging out. Send /hi or /start again.")
