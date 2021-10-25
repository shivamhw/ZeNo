from ZeNo import bot, users_dict
from ZeNo.modules import helper


@bot.callback_query_handler(func=lambda call: call.data in ["about", "faq"])
def classlinks_callback_handler(call):
    bot.answer_callback_query(call.id)
    res = helper.Pages.get_note(call.data)
    bot.send_message(call.message.chat.id, res)
