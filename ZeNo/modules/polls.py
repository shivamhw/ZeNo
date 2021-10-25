from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ZeNo import bot, poll_dict, users_dict
from ZeNo.modules.data import PollData


# @bot.callback_query_handler(func=lambda call: call.data == "create_poll")
def poll_callback_handler(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Remember few points")
    bot.send_message(call.message.chat.id, "1. User can create only one poll at a time")
    bot.send_message(call.message.chat.id, "2. For any poll only first reponse will be recorded")
    bot.send_message(call.message.chat.id, "3. Poll cannot have multiple responses ")
    bot.send_message(call.message.chat.id, "Enter briefy what the poll is about")
    bot.register_next_step_handler(call.message, create_poll)

@bot.callback_query_handler(func=lambda call: call.data == "show_poll")
def show_poll(call):
    bot.answer_callback_query(call.id)
    get_active_poll(call.message)




@bot.callback_query_handler(func=lambda call: "Active Poll" in call.data)
def active_poll_handler(call):
    bot.answer_callback_query(call.id)
    user = users_dict[call.message.chat.id]
    active_poll = user.active_poll
    user.current_poll = active_poll[call.data]
    display_poll(call.message)


@bot.callback_query_handler(func=lambda call: "Option" in call.data)
def options_handler(call):
    bot.answer_callback_query(call.id)
    user = users_dict[call.message.chat.id]
    current_poll = user.current_poll
    if user.answered_poll:
        user.answered_poll.append(current_poll)
    else:
        user.answered_poll = []
        user.answered_poll.append(current_poll)
    current_poll.response[call.data] += 1
    current_poll.total_response += 1
    get_poll_result(call.message)


def get_poll_result(message):
    user = users_dict[message.chat.id]
    current_poll = user.current_poll
    options = current_poll.options
    response = current_poll.response
    total_response = current_poll.total_response
    bot.send_message(message.chat.id, "Total " + str(total_response) + " response")
    for index, resp_count in current_poll.response.items():
        bot.send_message(message.chat.id, str(options[index]) + " - " + str((response[index] / total_response) * 100)+"%")
    user.current_poll = None


def display_poll(message):
    user = users_dict[message.chat.id]
    current_poll = user.current_poll
    answered_poll = user.answered_poll
    if bool(answered_poll) and current_poll in answered_poll:
        bot.send_message(message.chat.id, "You have already answered to this poll")
        get_poll_result(message)
    else:
        #bot.send_message(message.chat.id, str(current_poll.question))
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        for index, option in current_poll.options.items():
            markup.add(InlineKeyboardButton(text=option, callback_data=index))
        bot.send_message(message.chat.id, str(current_poll.question), reply_markup=markup)
 


def get_active_poll(message):
    user = users_dict[message.chat.id]
    active_poll = {}
    counter = 1
    if bool(poll_dict):
        for message_id, poll in poll_dict.items():
            active_poll["Active Poll " + str(counter)] = poll
            counter += 1
        user.active_poll = active_poll
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        for index, poll in active_poll.items():
            markup.add(InlineKeyboardButton(text=poll.about_poll, callback_data=index))
        bot.send_message(message.chat.id, "Choose a poll to answer", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "There is no active poll")


def get_options(message):
    current_option = message.text
    poll = poll_dict[message.chat.id]
    options = poll.options
    if not options:
        poll.options = {"Option "+str(poll.current_option_no): current_option}
    else:
        options["Option "+str(poll.current_option_no)] = current_option
        poll.options = options
    poll.current_option_no += 1
    if poll.current_option_no <= poll.no_of_options:
        bot.reply_to(message, "Give option " + str(poll.current_option_no))
        bot.register_next_step_handler(message, get_options)
    else:
        bot.send_message(message.chat.id, "Poll has been created")


def get_number_of_options(message):
    try:
        number_of_options = int(message.text)
        poll = poll_dict[message.chat.id]
        poll.no_of_options = number_of_options
        poll.current_option_no = 1
        response = {}
        for i in range(1, poll.no_of_options + 1):
            response["Option "+str(i)] = 0
        poll.response = response
        bot.reply_to(message, "Give option " + str(poll.current_option_no))
        bot.register_next_step_handler(message, get_options)
    except ValueError:
        bot.reply_to(message, "Give a valid input")
        bot.register_next_step_handler(message, get_number_of_options)


def get_poll_question(message):
    question = message.text
    poll = poll_dict[message.chat.id]
    poll.question = question
    bot.reply_to(message, "How many options you want?")
    bot.register_next_step_handler(message, get_number_of_options)


def create_poll(message):
    new_poll = PollData()
    poll_dict[message.chat.id] = new_poll
    about_poll = message.text
    poll = poll_dict[message.chat.id]
    poll.about_poll = about_poll
    bot.reply_to(message, "Give your question for poll!")
    bot.register_next_step_handler(message, get_poll_question)
