import requests
import json
from modules.dbhelper import save_marks
from ZeNo import bot, users_dict
from modules.helper import Parser
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
    "session" : 'JUL-20',
    "X-CSRFToken": '',
    "Referer": "https://aviral.iiita.ac.in/student/courses/"
}


@bot.callback_query_handler(func=lambda call: call.data.startswith("getmarks_"))
def callback_query(call):
    bot.answer_callback_query(call.id)
    if call.message.chat.id in users_dict:
        session = call.data[9:]
        get_marks(call.message, users_dict[call.message.chat.id],session)
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


@bot.callback_query_handler(func=lambda call: call.data == "aviral")
def callback_query(call):
    bot.answer_callback_query(call.id)
    if call.message.chat.id in users_dict:
        get_session(call.message, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")

@bot.callback_query_handler(func=lambda call: call.data == "aviral_spl")
def callback_query(call):
    bot.answer_callback_query(call.id)
    if call.message.chat.id in users_dict:
        get_special(call.message, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


def login(username, password, chat_id):
    main_session = requests.Session()
    main_session.get(aviral_login_url)
    # username = user.username
    # password = user.password
    post_body_login = {"username": username, "password": password}
    res = main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login))
    if res.text == '{"user_group": null}':
        return None
    user = User(username)
    jwt_res =  json.loads(main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login)).text)
    user.jwt_token = jwt_res['jwt_token']
    user.chat_id = chat_id

    user.session = jwt_res['session_id']

    user.cs_token = main_session.cookies.get_dict()['csrftoken']
    admins = ['mit2020122', 'mit2020080']
    if user.username in admins:
        user.is_admin = True
    # user.cookie = main_session.cookies
    user.save_userdata(get_userdata(user))
    # user_data = get_userdata(user)
    # user.name = user_data['first_name']
    # user.admission_year = user_data['admission_year']
    # user.program = user_data['program']
    return user


def get_userdata(user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    user_data = requests.get(aviral_details_api, headers=header_auth).json()
    print(f"Hello {user_data['first_name']}")
    return user_data

def get_session(message, user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    sessions = requests.get(url=aviral_sessions_api, headers=header_auth).json()
    print(sessions)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in sessions:
        markup.add(InlineKeyboardButton(i['name'], callback_data="getmarks_"+i['session_id']))
    bot.send_message(user.chat_id, "Which Session??", reply_markup=markup)

def get_special(message, user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    special_li = requests.get(aviral_details_api, headers=header_auth).json()
    # special_li = requests.get(aviral_specialize_api, headers=header_auth).json()
    try:
        spe = special_li['program']
      #  spe = Parser.special_parser(special_li)
    except Exception as e:
        spe = "Please fix" +str(e) +" in code."
    bot.send_message(message.chat.id, spe)

def get_marks(message, user, session):
    header_auth['session'] = session
    user.session = session
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    try:
        user_marks = requests.get(aviral_marks_api, headers=header_auth)
        user_data = requests.get(aviral_details_api, headers=header_auth).json()
        god_draft = json.loads(user_marks.text)
        for i in god_draft:
            print(f"Your marks in {i['name']} is {i['c1_marks']}")
            if(i['name'] not in user.enrolled_courses):
                user.enrolled_courses.append(i['name'])
        print(user.enrolled_courses)
        marks = Parser.marks_parser(god_draft)
        cgpi = Parser.cgpi_parser(user_data)
        bot.send_message(message.chat.id, marks)
        if marks != "\nNo Results for this session..":
            bot.send_message(message.chat.id, cgpi)
            save_marks(user, god_draft)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "something went wrong!!! please /start again")
        del users_dict[message.chat.id]
        user.del_user_db()
    #     del from DB and users_dict
    # try:
    #     userdata = get_userdata(user)
    #     DB.register_user(userdata, god_draft)
    #     analytics = DB.get_analytics(userdata["student_id"])
    #     analytics_message = "Students with less marks : " + str(analytics[0]) + "\n\n" \
    #                         + "Students with more marks : " + str(analytics[1]) + "\n\n" \
    #                         + "Students with equal marks : " + str(analytics[2])
    #     bot.send_message(message.chat.id, analytics_message)
    #     percentile = Parser.percentile(analytics)
    #     percentile_message = "Your class percentile is : " + str(percentile)
    #     bot.send_message(message.chat.id, percentile_message)
    # except Exception as e:
    #     print("Error occoured in DB " + str(e))
    return god_draft
