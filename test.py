import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import requests
import json


TELEGRAM_TOKEN = '1420627782:AAHOEG9qjDK-4qOEGJg7YFnWnp8ieIS6iD4'
bot = telebot.TeleBot(TELEGRAM_TOKEN)
users_dict = {}

class User:
    def __init__(self, name):
        self.username = name
        self.password = None


def login_user(message):
	# //bot.send_message()
	aviral_login_url = "https://aviral.iiita.ac.in/login"
	aviral_jwt_api_url = "https://aviral.iiita.ac.in/api/login/"
	aviral_marks_api = "https://aviral.iiita.ac.in/api/student/enrolled_courses/"
	aviral_details_api = "https://aviral.iiita.ac.in/api/student/dashboard/"
	jwt_token = None
	cs_token = None
	headers_single = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"
	}

	main_session = requests.Session()
	main_session.headers.update(headers_single)
	main_session.get(aviral_login_url)
	user = users_dict[message.chat.id]
	username = user.username
	password = user.password
	post_body_login = {"username": username, "password": password}
	main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login))
	jwt_token = json.loads(main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login)).text)['jwt_token']
	cs_token = main_session.cookies.get_dict()['csrftoken']
	header_dikkt = {
		"Host": "aviral.iiita.ac.in",
		"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
		"Accept": 'application/json, text/plain, */*',
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Authorization": jwt_token,
		"session": "JUL-20",
		"X-CSRFToken": cs_token,
		"Referer": "https://aviral.iiita.ac.in/student/courses/"
	}
	user_data = main_session.get(aviral_details_api, headers=header_dikkt).json()
	bot.send_message(message.chat.id, f"Hello {user_data['first_name']}")
	i_think = main_session.get(aviral_marks_api, headers=header_dikkt)
	god_draft = json.loads(i_think.text)
	for i in god_draft:
		bot.send_message(message.chat.id, f"Your marks in {i['name']} is {i['c1_marks']}")


def gen_markup_login():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Login Now", callback_data="main_login"),
                               InlineKeyboardButton("No Thanks", callback_data="cancel"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "main_login":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id , "please enter you login")
        bot.register_next_step_handler(call.message, get_username)
    elif call.data == "aviral":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id , "aviral id ")
        # bot.register_next_step_handler(call.message, login_user1)
        login_user(call.message)
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
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Aviral Numbers", callback_data="aviral"))
    bot.reply_to(message, 'Kya kre', reply_markup=markup)
    bot.register_next_step_handler(message, login_user)

@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    hello_msg = ("Hey, I am ZeNo. I was created to save your time so you can do your assignments with one hand!\n"
				 "Please wait while i check your status.....")
    bot.send_message(message.chat.id, hello_msg)
    # bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())
    if(True):
        # bot.send_message(message.chat.id, message)
        bot.send_message(message.chat.id, "ohhh! you are not registered with us.\nWant to login??")
        bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup_login())
bot.polling(none_stop=True)