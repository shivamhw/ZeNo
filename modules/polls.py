from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from ZeNo import bot
from modules.data import PollData
from random import randint
active_polls = {}

@bot.callback_query_handler(func=lambda call: call.data == ["create_poll", "show_poll"])
def poll_callback_handler(call):
    if call.data == "create_poll":
        create_poll(call.message)
    elif call.data == "show_poll":
        show_active_polls(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "poll_yes")
def broadcast_handler(call):
    bot.answer_callback_query(call.id)
    add_options()




def create_poll(message):
    new_poll = PollData()
    new_poll.id = randint(0, 100000)
    active_polls[new_poll.id] = new_poll
    reply = bot.send_message(message.chat.id, "What is you question for poll???")
    bot.register_next_step_handler(reply, add_question, new_poll)

def add_question(message, new_poll):
    new_poll.question = message.text
    reply = bot.reply_to(message, "how many options??")
    bot.register_next_step_handler(reply, add_options, new_poll)
    # markup = InlineKeyboardMarkup()
    # markup.row_width = 2
    # markup.add(InlineKeyboardButton("sure", callback_data="poll_yes"), InlineKeyboardButton("Cancel", callback_data="no_a"))
    # bot.send_message(message.chat.id, "Please select", reply_markup=markup)

def add_options(message, new_poll):
    options = message.text
    for i in range(1, options+1):
        bot.send_message(message.chat.id, "add option")
        