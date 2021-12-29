import telebot
import requests as req
from bs4 import BeautifulSoup
from datetime import datetime
from token_telegram import token

#Import token from token_telegram.py
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help'])
def welcome(message):
    bot.reply_to(message, f"Привет, {message.from_user.username}!\n\
Просто введите любое слово для поиска книги на fantlab."
                 )
    with open('text_log', 'a') as text:    
        text.write(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S '))
        text.write(f"You message: '{message.text}' \n")
   
    
#Handle sticker and returne it with emoji
@bot.message_handler(content_types=['sticker'])
def stiker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)
    bot.reply_to(message, f"You sticker mean {message.sticker.emoji}")
    

@bot.message_handler(func=lambda message: True)  
def book_find(message):
    
    '''Handle key word from user, and search relatible book on fantlab.ru.
       
       Return three most relevant result
    
    '''
    
    request = req.get("https://fantlab.ru/searchmain?searchstr=" + message.text)
#    with open('fantlab_log', 'a') as text:
#    text.write(request.text)

    soup = BeautifulSoup(request.text, 'html.parser')
    result = soup.find_all(class_='search-block works')
    if result == []:
        bot.reply_to(message, 'Ничего не найдено')
    else:
        for element in result:
            title = element.find_all(class_='title')
            if len(title) > 3:
                number_elements = 3
            else:
                number_elements = len(title)
            for i in title:
                t = str(i.find('a'))
                t = "fantlab.ru" + t[t.find('/'):t.rfind('"')]
                bot.reply_to(message, t)
                number_elements -= 1
                if number_elements == 0:
                    break
                
                
bot.polling(none_stop=True, interval=1)
