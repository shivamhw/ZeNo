import time

import requests
import json
from modules.dbhelper import save_marks,set_flag
from ZeNo import bot, users_dict
import sys
from modules.helper import Parser, is_reg
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from modules.data import User

# API for requests
aviral_login_url = "https://aviral.iiita.ac.in/login"
aviral_jwt_api_url = "https://aviral.iiita.ac.in/api/login/"
aviral_marks_api = "https://aviral.iiita.ac.in/api/student/enrolled_courses/"
aviral_details_api = "https://aviral.iiita.ac.in/api/student/dashboard/"
aviral_sessions_api = "https://aviral.iiita.ac.in/api/sessions/"
aviral_specialize_api = "https://aviral.iiita.ac.in/api/student/mtechspls/status/"

# Global Variables
header_auth = {
    "Host": "aviral.iiita.ac.in",
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
    "Accept": 'application/json, text/plain, */*',
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Authorization": '',
    "session": '',
    "X-CSRFToken": '',
    "Referer": "https://aviral.iiita.ac.in/student/courses/"
}


@bot.callback_query_handler(func=lambda call: call.data.startswith("getmarks_"))
def callback_query(call):
    bot.answer_callback_query(call.id)
    if is_reg(call.message):
        session = call.data[9:]
        get_marks(call.message, users_dict[call.message.chat.id], session)
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


@bot.callback_query_handler(func=lambda call: call.data == "aviral")
def callback_query(call):
    bot.answer_callback_query(call.id)
    if is_reg(call.message):
        get_session(call.message, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def callback_query(call):
    bot.answer_callback_query(call.id)
    if is_reg(call.message):
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Please click /hi again")
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


@bot.callback_query_handler(func=lambda call: call.data == "enable_analytics")
def callback_query(call):
    bot.answer_callback_query(call.id)
    if is_reg(call.message):
        enable_analytics(call.message, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


@bot.callback_query_handler(func=lambda call: call.data.startswith("enable_analytics_"))
def callback_query(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.id)
    if is_reg(call.message):
        analytics_manager(call.data, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


@bot.callback_query_handler(func=lambda call: call.data == "aviral_spl")
def callback_query(call):
    bot.answenotr_callback_query(call.id)
    if call.message.chat.id in users_dict:
        get_special(call.message, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


def login(username, password, chat_id):
    main_session = requests.Session()
    post_body_login = {"username": username, "password": password}
    try:
        main_session.get(aviral_login_url)
        res = main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login), timeout=5)
        if res.text == '{"user_group": null}':
            return None
        jwt_res = json.loads(main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login)).text)
        user = User(username)
        user.jwt_token = jwt_res['jwt_token']
        user.chat_id = chat_id
        user.session = jwt_res['session_id']
        user.cs_token = main_session.cookies.get_dict()['csrftoken']
        try:
            user.save_userdata(get_userdata(user))
        except:
            print("error getting userdata")
        print("resturn user")
        return user
    except:
        print(sys.exc_info())
        return None


def get_userdata(user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    header_auth['session'] = user.session
    user_data = requests.get(aviral_details_api, headers=header_auth).json()
    print(f"Hello {user_data['first_name']}")
    return user_data


def get_session(message, user):
    msg = bot.send_message(user.chat_id, "Getting session details.....")
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    header_auth['session'] = user.session
    try:
        sessions = requests.get(url=aviral_sessions_api, headers=header_auth).json()
        print(sessions)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in sessions:
            markup.add(InlineKeyboardButton(i['name'], callback_data="getmarks_" + i['session_id']))
        bot.send_message(user.chat_id, "Which Session??", reply_markup=markup)
    except Exception as e:
        print("error getting session")
        print(str(e))
        bot.send_message(user.chat_id, "error getting session details. /start again")
    bot.delete_message(msg.chat.id, msg.id)


def get_special(message, user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    special_li = requests.get(aviral_details_api, headers=header_auth).json()
    try:
        spe = special_li['program']
    except Exception as e:
        spe = "Please fix" + str(e) + " in code."
    bot.send_message(message.chat.id, spe)


def get_marks(message, user, session):
    bot.delete_message(message.chat.id, message.id)
    wait_msg = bot.send_message(message.chat.id, "Getting marks for " + session + " Session....")
    header_auth['session'] = session
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    god_draft = None
    try:
        user_marks = requests.get(aviral_marks_api, headers=header_auth)
        user_data = requests.get(aviral_details_api, headers=header_auth).json()
        god_draft = json.loads(user_marks.text)
        for i in god_draft:
            print(f"Your marks in {i['name']} is {i['c1_marks']}")
            if i['name'] not in user.enrolled_courses:
                user.enrolled_courses.append(i['name'])
        marks = Parser.marks_parser(god_draft, user.username, session, analytics=user.flags['analytics_enabled'])
        cgpi = Parser.cgpi_parser(user_data, session, analytics=user.flags['analytics_enabled'])
        bot.send_message(message.chat.id, marks)
        if marks != "\nNo Results for this session..":
            bot.send_message(message.chat.id, cgpi)
            if user.flags['analytics_enabled']:
                save_marks(user, session, god_draft)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "something went wrong!!! please /start again")
        del users_dict[message.chat.id]
        user.del_user_db()
    bot.delete_message(wait_msg.chat.id, wait_msg.id)
    return god_draft


def enable_analytics(message, user):

    if user.flags['analytics_enabled']:
        yes_msg = "You have analytics enabled.\n\n Analytics do not share anything and does not even have any open api " \
                  "to access any records, as aviral dont provide any analytics so we have" \
                  + "to maintain our own little DB to give you analytics. It is not shared and all the code is hosted " \
                    "on " \
                    "github so you can ensure that there is no API support for any privacy" \
                  + " invading calls."
        msg = bot.send_message(message.chat.id, yes_msg)
        # time.sleep(10)
        # bot.delete_message(message.chat.id, msg.id)
        yes_msg = "But still if you dont want to contribute to rank analytics then it okay too. You can opt out from " \
                  "here. You can still use ZeNo as before but without analytics. \n\n"
        yes_msg += "Here are some things to keep in mind when opting out.\n" \
                   + "1. You wont be able to see your ranks also.\n" \
                   + "2. Your old data will take time to flush out from system but your new marks will not be stored " \
                     "from immediate effect.\n" \
                   + "3. As of now you can't opt in one you opt out.\n\n\n\n Please wait......"
        msg1 = bot.send_message(message.chat.id, yes_msg)
        time.sleep(10)
        bot.delete_message(message.chat.id, msg.id)
        bot.delete_message(message.chat.id, msg1.id)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Disable Analytics for me", callback_data="enable_analytics_no"), InlineKeyboardButton("Cancel", callback_data="cancel"))
        bot.send_message(message.chat.id, "Do you want to opt out?", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Enable Analytics for me", callback_data="enable_analytics_yes"), InlineKeyboardButton("Cancel", callback_data="cancel"))
        bot.send_message(message.chat.id, "Do you want to opt in?", reply_markup=markup)


def analytics_manager(data, user):
    if data == "enable_analytics_no":
        user.flags['analytics_enabled'] = False
        set_flag(user.username, "analytics_enabled", False)
        msg = bot.send_message(user.chat_id, "okay, Your new marks will not be used for analytics from now.")
        time.sleep(5)
        bot.delete_message(user.chat_id, msg.id)
    if data == "enable_analytics_yes":
        user.flags['analytics_enabled'] = True
        set_flag(user.username, "analytics_enabled", True)
        msg = bot.send_message(user.chat_id, "okay, but opting in and out multiple time will block the feature for you.")
        time.sleep(5)
        bot.delete_message(user.chat_id, msg.id)
