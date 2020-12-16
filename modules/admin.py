from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ZeNo import bot, users_dict
from modules import classlinks
amodules = {"broadcast": "Broadcast",
            "change_classlinks": "Change Class Links"}
broadcast_msg = "testB"


# modules handler
@bot.callback_query_handler(func=lambda call: call.data == "broadcast_yes")
def broadcast_handler(call):
    bot.answer_callback_query(call.id)
    broadcast()


# main handlers
@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
def admin_panel_callback(call):
    bot.answer_callback_query(call.id)
    admin_panel(call.message)


@bot.callback_query_handler(func=lambda call: call.data in get_modules())
def handler_callback(call):
    bot.answer_callback_query(call.id)
    handle(call.message, call.data)


def handle(message, key):
    if key == 'broadcast':
        bot.send_message(message.chat.id, " Please type your message.")
        bot.register_next_step_handler(message, get_msg)
    if key == "change_classlinks":
        classlinks.set_classlinks(message)

def get_modules():
    return amodules

def get_msg(message):
    global broadcast_msg
    broadcast_msg = message.text
    bot.reply_to(message, "Preview of message:")
    bot.send_message(message.chat.id, broadcast_msg)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("sure", callback_data="broadcast_yes"),
               InlineKeyboardButton("Cancel", callback_data="no_a"))
    bot.send_message(message.chat.id, "Please select", reply_markup=markup)


def broadcast():
    for i in users_dict:
        bot.send_message(i, broadcast_msg)


def admin_panel(message):
    bot.send_message(message.chat.id, "Admins have superpowers!!! Use it wisely.")
    markup = InlineKeyboardMarkup()
    for i, j in get_modules().items():
        markup.add(InlineKeyboardButton(j, callback_data=i))
    bot.send_message(message.chat.id, "Here are some things only admin can do", reply_markup=markup)
