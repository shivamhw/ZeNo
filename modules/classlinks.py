from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ZeNo import bot, users_dict


links = {
    "Mathematics for IT": {"WebX Link": "https://iiita.webex.com/iiita/j.php?MTID=m0d3e4cf74627def4662279471fb4266c"},
    "Advanced Data Structures and Algorithms": {"Google Meet": "http://meet.google.com/yiw-nqfg-yxa"},
    "Programming Practices": {"WebX": "https://iiita.webex.com/iiita/j.php?MTID=m7528a6c828480999a4e390b597f4c6e7"},
    "Research Methodology": {"Google Meet": "https://meet.google.com/lookup/brhkymcmhd",
                             "Google Meet 2": "https://meet.google.com/eub-qxkg-skw"}}


@bot.callback_query_handler(func=lambda call: call.data == "classlinks")
def classlinks_callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.message.chat.id in users_dict:
        user = users_dict[call.message.chat.id]
        user.request_no = 0
        get_classlinks(call.message)
    else:
        bot.send_message(call.message.chat.id, "Please /start again")


def get_classlinks(message):
    if message.chat.id not in users_dict:
        bot.send_message(message.chat.id, "Please click /start again....")
    else:
        user = users_dict[message.chat.id]
        for course in user.enrolled_courses:
            markup = InlineKeyboardMarkup()
            if course in links.keys():
                local_links = links[course]
                markup.row_width = len(local_links.keys())
                for text, url in local_links.items():
                    markup.add(InlineKeyboardButton(text, url=url))
            else:
                markup.add(InlineKeyboardButton("No links found"))
            bot.send_message(message.chat.id, course, reply_markup=markup)


def set_classlinks(message):
    markup = InlineKeyboardMarkup()
    for course in users_dict[message.chat.id].enrolled_courses:
        markup.add(InlineKeyboardButton(course, callback_data="link_"+course))
    bot.send_message(message.chat.id, "which one??", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("link_"))
    def linkchanger(call):
        bot.answer_callback_query(call.id)
        course_to_change = call.data[5:]
        markup_yes_no = InlineKeyboardMarkup()
        markup_yes_no.row_width = 2
        markup_yes_no.add(InlineKeyboardButton("Add link", callback_data="addlink_"+course_to_change),
                          InlineKeyboardButton('Remove Link', callback_data="remlink_"+course_to_change))
        bot.send_message(call.message.chat.id, "please choose for "+course_to_change, reply_markup=markup_yes_no)

        @bot.callback_query_handler(func=lambda call: call.data.startswith("addlink_") or call.data.startswith("remlink_"))
        def tatticode(call):
            bot.answer_callback_query(call.id)
            course_name = call.data[8:]
            if call.data[0] == "a":
                msg = bot.send_message(call.message.chat.id, "please add a name for link in "+course_name)
                bot.register_next_step_handler(msg, get_name, course_name)
            elif call.data[0] == "r":
                print("remo")
                local_links = links[course_name]
                markup = InlineKeyboardMarkup()
                markup.row_width = len(local_links.keys())
                for text, url in local_links.items():
                    markup.add(InlineKeyboardButton(text, callback_data="linkrem_"+text))
                bot.send_message(call.message.chat.id, "please select a link to delete..", reply_markup=markup)

        def get_name(msg, course_name):
            li = msg.text
            bot.send_message(msg.chat.id, "this link will be added as " + li + " for "+course_name+" \nPlease send new link now....")
            bot.register_next_step_handler(msg, get_link, course_name, li)

        def get_link(msg, course_name, lin_nm):
            li = msg.text
            bot.send_message(msg.chat.id, "this will be added as new link " + lin_nm + " for "+course_name)
            links[course_name][lin_nm] = li
