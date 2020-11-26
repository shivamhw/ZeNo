import requests
import json
from dbhelper import Dbhelper

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


def login(user):
	main_session = requests.Session()
	main_session.get(aviral_login_url)
	db = Dbhelper() #Create Db session
	username = user.username
	password = user.password
	post_body_login = {"username": username, "password": password}
	res = main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login))
	if(res.text == '{"user_group": null}'):
		return False

	user.jwt_token = json.loads(main_session.post(aviral_jwt_api_url, data=json.dumps(post_body_login)).text)['jwt_token']
	user.cs_token = main_session.cookies.get_dict()['csrftoken']
	user.cookie = main_session.cookies
	userData = get_userdata(user)
	user.name = userData['first_name']
	user.is_admin = db.is_admin(user.username) # to be done by nikhil
	marks = get_marks(user)
	db.register_user(userData, marks)  # just for db to be done by nikhil
	return True

def get_userdata(user):
	header_auth['Authorization'] = user.jwt_token
	header_auth['X-CSRFToken'] = user.cs_token
	user_data = requests.get(aviral_details_api, headers=header_auth, cookies=user.cookie).json()
	print(f"Hello {user_data['first_name']}")
	return user_data

def get_marks(user):
	header_auth['Authorization'] = user.jwt_token
	header_auth['X-CSRFToken'] = user.cs_token
	user_marks = requests.get(aviral_marks_api, headers=header_auth)
	god_draft = json.loads(user_marks.text)
	for i in god_draft:
		print(f"Your marks in {i['name']} is {i['c1_marks']}")
	return god_draft
