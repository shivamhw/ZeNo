from modules import admin, classlinks
from ZeNo import bot, users_dict, poll_dict
from modules.login import front_page
from modules.data import PollData
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


# main button event handler
@bot.callback_query_handler(func=lambda call: False)
def callback_query(call):
    if call.data == "createpoll":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Enter briefly  about poll")
        bot.register_next_step_handler(call.message, create_poll)
    elif call.data == "activepoll":
        if call.message.chat.id in users_dict:
            bot.register_next_step_handler(call.message, get_active_poll)


#### Handler functions





##Helper functions



def get_poll_result(message):
    user = users_dict[message.chat.id]
    current_poll = user.current_poll
    options = current_poll.options
    response = current_poll.response
    total_response = current_poll.total_response
    for index, resp_count in current_poll.response.items():
        bot.send_message(message, str(options[index])+ " - " + str((response[index]/total_reponse)*100))
    user.current_poll = None


def get_response(message):
    response = message.text
    user = users_dict[message.chat.id]
    current_poll = user.current_poll
    if user.answered_poll is  not None:
        user.answered_poll.append(user.current_poll)
    else:
        user.answered_poll = list(user.current_poll)
    current_poll.response[response] += 1
    current_poll.total_response += 1
    bot.register_next_step_handler(message, get_poll_result)


def display_poll(message):
    user = users_dict[message.chat.id]
    current_poll = user.current_poll
    answered_poll = user.answered_poll
    bot.send_message(message.chat.id, current_poll.question)
    for index, option in current_poll.options.items():
        bot.send_message(message.chat.id, str(index)+" - "+ str(option))
    if  current_poll in answered_poll:
         bot.register_next_step_handler(message, get_poll_result)
    else:
         bot.reply_to(message, "Enter your response")
         bot.register_next_step_handler(message, get_response)


def get_active_poll(message):
    user = users_dict[message.chat.id]
    active_polls = {}
    counter = 1
    for id in poll_dict.values():
        active_polls[counter] = id
        counter += 1
    for index, poll in active_polls.items():
        bot.send_message(message.chat.id, str(index)+"-"+str(poll.about_poll))
    bot.send_message(message.chat.id, "Choose poll")
    poll_index = message.text
    user.current_poll = active_poll[poll_index]
    bot.register_next_step_handler(message, display_poll)

def get_option(message, option_no):
    bot.send_message(message.chat.id, "Enter option "+str(option_no))
    option = message.text
    return option

def get_poll_question(message):
    question = message.text
    poll = poll_dict[message.chat.id]
    poll.question = question
    number_of_option = message.text+1
    options = {}
    response = {}
    for i in range(1, number_of_option):
        options[i] = get_option(message, i)
        response[i] = 0
    poll.options = options
    poll.response = response

def get_about_poll(message):
    about_poll = message.text
    poll = poll_dict[message.chat.id]
    poll.about_poll = about_poll
    bot.reply_to(message, "Enter number of options")
    bot.register_next_step_handler(message, get_poll_question)

def create_poll(message):
    new_poll = PollData()
    poll_dict[message.chat.id] = new_poll
    bot.reply_to(message, "Enter poll question")
    bot.regiester_next_step_handler(message, get_about_poll)

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

