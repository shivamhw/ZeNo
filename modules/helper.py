from ZeNo import bot, users_dict
from modules.dbhelper import is_in_db, get_user_db, get_analytics


class emojis:
    emoji_db = {
        "first_rank": "🥇",
        "second_rank": "🥈",
        "third_rank": "🥉",
        "other_rank": "🎉",
        "bar_chart": "📊",
        "lock_key": "🔐",
        "question_mark": "❓"
    }

    def get_emoji(id):
        try:
            return emojis.emoji_db[id]
        except:
            return None


class Parser:
    def marks_parser(raw_data, username, session, analytics=False):
        output_string = 'Results: \n\n'
        for i in raw_data:
            marks_cur = 0
            output_string += str(i['name']) + " : \n" \
                             + i['c1_marks'] + ' | ' \
                             + i['c2_marks'] + ' | ' \
                             + i['c3_marks'] + ' = ' \
                             + i['total'] + '\n' \
                             + "GPA = " + i['gpa'] + '\n'
            if analytics:
                if i['c1_marks'] != "N/A":
                    marks_cur += float(i['c1_marks'])
                if i['c2_marks'] != "N/A":
                    marks_cur += float(i['c2_marks'])
                if i['c3_marks'] != "N/A":
                    marks_cur += float(i['c3_marks'])
                rank, total = get_analytics(session, username, i['name'], marks_cur)
                output_string += "Rank: "
                if rank == 1:
                    output_string += emojis.get_emoji("first_rank")
                if rank == 2:
                    output_string += emojis.get_emoji("second_rank")
                if rank == 3:
                    output_string += emojis.get_emoji("third_rank")
                if rank > 3:
                    output_string += emojis.get_emoji("other_rank")
                output_string += str(rank) + "/" + str(total)
            output_string += '\n\n'
        if output_string == 'Results: \n\n':
            output_string = "\nNo Results for this session.."

        return output_string

    def special_parser(data):
        output_string = "Current allotment:\n\n"
        for i, j in data.items():
            output_string += str(i) + " : " + str(j) + "\n"
        return output_string

    def cgpi_parser(user_data, session, analytics=False):
        output_string = "Final Results: \n"
        # output_string += "Semester : " + user_data['semester']
        output_string += "\nCGPI : " + str(user_data['cgpi'])
        output_string += "\nCompleted/Total Credits : " + str(user_data['completed_total']) + "/" + str(
            user_data['total_credits'])
        return output_string

    def sgpi_parser(user_data, session, analytics=False):
        output_string = "Semester Results: \n"
        try:
            for i in user_data['data']:
                output_string += "\nSemester : " + str(i['semester'])
                output_string += "\nsgpi : " + str(i['sgpi'])
        except:
            output_string = "error parsing semester results."
        return output_string

    def percentile(marks_analytics):
        total_students = marks_analytics[0] + marks_analytics[1] + marks_analytics[2] + 1
        percentile = (marks_analytics[0] + marks_analytics[2] + 1) / total_students * 100
        return percentile


class Pages:
    faq = ("1. Why use Zeno?"
           "\n\nAns. it is fast than aviral website and provides information more efficiently than any whatsapp group,"
           "\nbut the main reason to use Zeno is because you can view code and tinker around with stuff. "
           "You can see how a fun little project can scale or fail at production enviroment and try to fix the problems yourself"
           "\n\n2. What about privacy?"
           "\n\nAns. Zeno works with token so it just saves your session with aviral. at no point of time your password is stored in any DB."
           )
    about = ("Zeno started as a fun project but became a part of developers life."
             "\n\nIt is here to provide a single point of contact for IIITA students so they dont need to switch between different platform to get something done."
             "\n\nGitHub : bit.ly/zeno-iiita "
             )
    pages = {'about': about, 'faq': faq}

    def get_note(note):
        return Pages.pages[note]


def is_reg(message):
    if (message.chat.id in users_dict):
        return True
    elif (is_in_db(message.chat.id)):
        bot.send_message(message.chat.id, "not in cache but trying to get it from db....")
        user = get_user_db(message.chat.id)
        users_dict[message.chat.id] = user
        return True
    return False
