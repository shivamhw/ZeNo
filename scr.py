import telebot

bot = telebot.TeleBot("1422837559:AAEWGEujmJWy_cgvZUCChEGMleclYWdJ1OY")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	msg = bot.send_message(message.chat.id, "nisafoasj")
	bot.edit_message_text("nikola", chat_id=msg.chat.id, message_id=msg.id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()