import requests
import json
import telebot


bot_token = "1420627782:AAHOEG9qjDK-4qOEGJg7YFnWnp8ieIS6iD4"
aviral_login_url = "https://aviral.iiita.ac.in/login"
aviral_jwt_api_url = "https://aviral.iiita.ac.in/api/login/"
aviral_marks_api = "https://aviral.iiita.ac.in/api/student/enrolled_courses/"
aviral_details_api = "https://aviral.iiita.ac.in/api/student/dashboard/"
jwt_token = None
cs_token = None

main_session = requests.Session()
main_session.get(aviral_login_url)
username = input("Username DO ")
password = input("Password DO ")
post_body_login = {"username":username,"password":password}
tes = main_session.post(aviral_jwt_api_url, data = json.dumps(post_body_login))
jwt_token = json.loads(main_session.post(aviral_jwt_api_url, data = json.dumps(post_body_login)).text)['jwt_token']
cs_token = main_session.cookies.get_dict()['csrftoken']
header_dikkt = {
    "Host": "aviral.iiita.ac.in",
    "User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
    "Accept": 'application/json, text/plain, */*',
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding" : "gzip, deflate, br",
    "Authorization": jwt_token,
    "session": "JUL-20",
    "X-CSRFToken" : cs_token,
    "Referer": "https://aviral.iiita.ac.in/student/courses/"
}
user_data = main_session.get(aviral_details_api, headers=header_dikkt).json()
print(f"Hello {user_data['first_name']}")
i_think = main_session.get(aviral_marks_api, headers = header_dikkt)
god_draft = json.loads(i_think.text)
for i in god_draft:
    print(f"Your marks in {i['name']} is {i['c1_marks']}")
