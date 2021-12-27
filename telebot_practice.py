import telebot
from token_telegram import token

#Import token from token_telegram.py
bot = telebot.TeleBot(token)

#Handle command /help and return "hello message"
@bot.message_handler(commands=['help'])
def welcome(message):
    bot.reply_to(message, 'Hi, ' + message.from_user.username + '!')


#Handle sticker and returne it with emoji
@bot.message_handler(content_types=['sticker'])
def stiker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)
    bot.reply_to(message, "You sticker mean" + message.sticker.emoji)
    

# handle text send echo reply and save it to text_log
@bot.message_handler(func=lambda message: True)  
def echo_all(message):
    bot.reply_to(message, message.text)
    with open('text_log', 'a') as text:
        text.write(message.text + '\n')
    
    
bot.polling(none_stop=True, interval=1)
