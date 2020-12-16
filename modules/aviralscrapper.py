import requests
import json
from ZeNo import bot, users_dict, DB
from modules.helper import Parser

# API for requests
aviral_login_url = "https://aviral.iiita.ac.in/login"
aviral_jwt_api_url = "https://aviral.iiita.ac.in/api/login/"
aviral_marks_api = "https://aviral.iiita.ac.in/api/student/enrolled_courses/"
aviral_details_api = "https://aviral.iiita.ac.in/api/student/dashboard/"

# Global Variables
header_auth = {
    "Host": "aviral.iiita.ac.in",
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
    "Accept": 'application/json, text/plain, */*',
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Authorization": '',
    "session": "JUL-20",
    "X-CSRFToken": '',
    "Referer": "https://aviral.iiita.ac.in/student/courses/"
}


@bot.callback_query_handler(func=lambda call: call.data == "aviral")
def callback_query(call):
    bot.answer_callback_query(call.id)
    if call.message.chat.id in users_dict:
        get_marks(call.message, users_dict[call.message.chat.id])
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


def login(user):
    main_session = requests.Session()
    main_session.get(aviral_login_url)
    username = user.username
    password = user.password
    post_body_login = {"username": username, "password": password}
    res = main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login))
    if res.text == '{"user_group": null}':
        return False
    user.jwt_token = json.loads(main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login)).text)[
        'jwt_token']
    user.cs_token = main_session.cookies.get_dict()['csrftoken']
    user.cookie = main_session.cookies
    user_data = get_userdata(user)
    user.name = user_data['first_name']
    return True


def get_userdata(user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    user_data = requests.get(aviral_details_api, headers=header_auth, cookies=user.cookie).json()
    print(f"Hello {user_data['first_name']}")
    return user_data


def get_marks(message, user):
    header_auth['Authorization'] = user.jwt_token
    header_auth['X-CSRFToken'] = user.cs_token
    user_marks = requests.get(aviral_marks_api, headers=header_auth)
    god_draft = json.loads(user_marks.text)
    try:
        userdata = get_userdata(user)
        DB.register_user(userdata, god_draft)
        analytics = DB.get_analytics(userdata["student_id"])
        analytics_message = "Students with less marks : " + str(analytics[0]) + "\n\n" \
                            + "Students with more marks : " + str(analytics[1]) + "\n\n" \
                            + "Students with equal marks : " + str(analytics[2])
        bot.send_message(message.chat.id, analytics_message)
        percentile = Parser.percentile(analytics)
        percentile_message = "Your class percentile is : " + str(percentile)
        bot.send_message(message.chat.id, percentile_message)
    except Exception as e:
        print("Error occoured in DB " + str(e))
    return god_draft
