#Напишите обработчик, который на сообщения с фотографией будет отвечать сообщением «Nice meme XDD». Бот должен отвечать не отдельным сообщением, а с привязкой к картинке.

import telebot
TOKEN = 'SomeToken'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_method(message):
    bot.reply_to(message, 'Nice meme XDD')

bot.polling(none_stop=True)