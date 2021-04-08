#Допишите обработчик так, чтобы он из сообщения брал username и выдавал приветственное сообщение с привязкой к пользователю.

import telebot
TOKEN = 'SomeToken'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def handle_method(message):
    username = str(message.chat.username) if str(message.chat.username) != 'None' else str(message.chat.first_name)
    bot.send_message(message.chat.id, 'Привет ' + username + '!')

bot.polling(none_stop=True)