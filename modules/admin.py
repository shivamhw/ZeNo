from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = None
amodules = {"broadcast" : "Broadcast"}
broadcast_msg = "testB"

def handle(bot1, users_dict, message, key):
    global bot
    bot = bot1
    if key == 'broadcast':
        bot.send_message(message.chat.id, " Please type your message.")
        bot.register_next_step_handler(message, get_msg)

def get_modules():
    return amodules

def get_msg(message):
    global  broadcast_msg
    broadcast_msg = message.text
    bot.reply_to(message, "Preview of message:")
    bot.send_message(message.chat.id, broadcast_msg)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("sure", callback_data="sure_a"), InlineKeyboardButton("Cancel", callback_data="no_a"))
    bot.send_message(message.chat.id, "Please select", reply_markup=markup)

def broadcast(bot, users_dict):
    for i in users_dict:
        bot.send_message(i, broadcast_msg)

