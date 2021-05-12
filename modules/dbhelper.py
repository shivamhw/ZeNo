from ZeNo import MONGO
from ZeNo.modules.data import User


def save_user_db(user):
    try:
        MONGO.users.insert_one(
            {
                'chat_id': user.chat_id,
                'username': user.username,
                'name': user.name,
                'section': user.section,
                'semester': user.semester,
                'is_admin': user.is_admin,
                'admission_year': user.admission_year,
                'program': user.program,
                'jwt_token': user.jwt_token,
                'cs_token': user.cs_token,
                'session': user.session
            }
        )
    except:
        print("error while saving user")


def del_user(user):
    MONGO.users.delete_many({"chat_id": user.chat_id})


def is_in_db(chat_id):
    user = MONGO.users.find_one({'chat_id': chat_id})
    if user is None:
        return False
    else:
        return True


def save_marks(user, session, marks):
    user_db = MONGO.marks.find_one({'username': user.username, 'session': session})
    if user_db is None:
        MONGO.marks.insert_one({
            'username': user.username,
            'session': session,
            'marks': marks
        })
    else:
        MONGO.marks.remove(
            {
                'username': user.username,
                'session': session
            }
        )
        MONGO.marks.insert_one({
            'username': user.username,
            'session': session,
            'marks': marks
        })
    return True


def number_of_users():
    u = MONGO.users.count()
    return u


def get_all_users():
    users = MONGO.users.find({})
    output = []
    for i in users:
        output.append(str(i['chat_id']))
    return output


def get_user_db(chat_id):
    try:
        u = MONGO.users.find_one({'chat_id': chat_id})
        user = User(u['username'])
        user.chat_id = u['chat_id']
        user.username = u['username']
        user.name = u['name']
        user.session = u['session']
        user.section = u['section']
        user.semester = u['semester']
        user.is_admin = u['is_admin']
        user.admission_year = u['admission_year']
        user.program = u['program']
        user.jwt_token = u['jwt_token']
        user.cs_token = u['cs_token']
    except:
        print("error getting user from db")
    return user
