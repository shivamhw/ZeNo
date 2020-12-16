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
    raw = links
    for i, j in raw.items():
        markup = InlineKeyboardMarkup()
        markup.row_width = len(j.keys())
        for text, res in j.items():
            markup.add(InlineKeyboardButton(text, url=res))
        bot.send_message(message.chat.id, i, reply_markup=markup)
