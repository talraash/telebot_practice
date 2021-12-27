import telebot
from token_telegram import token


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help'])
def welcome(message):
    bot.reply_to(message, 'Hi, ' + message.from_user.username + '!')
    

# handle text send echo reply and save it to text_log
@bot.message_handler(func=lambda message: True)  
def echo_all(message):
    bot.reply_to(message, message.text)
    with open('text_log', 'a') as text:
        text.write(message.text + '\n')
    
    
bot.polling(none_stop=True, interval=2)