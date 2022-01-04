import asyncio

from aiogram import Bot, Dispatcher, executor, types
from telegram_token import token
import requests as req
import aiohttp
from aiogram.utils.emoji import emojize
from bs4 import BeautifulSoup

bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def cat():
    request = req.get("http://aws.random.cat/meow")
    file = request.json()
    file = file['file']
    return str(file)


@dp.message_handler()
async def get_fantlab_content(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://fantlab.ru/searchmain?searchstr=' + message.text) as respond:
            text = await respond.read()
    soup = BeautifulSoup(text.decode('utf-8'), 'lxml')
    info = soup.find_all(class_='search-block works')
    for elements in info:
        title = elements.find_all_next(class_='title')
        if len(title) > 3:
            number_elements = 3
        else:
            number_elements = len(title)
        for i in title:
            t = str(i.find('a'))
            t = "fantlab.ru" + t[t.find('/'):t.rfind('"')]
            await message.answer(t)
            number_elements -= 1
            if number_elements == 0:
                break


@dp.message_handler(commands='cat')
async def reply(message: types.Message):
    file = cat()
    await bot.send_photo(message.chat.id, file)


@dp.message_handler(commands='help')
async def reply2(message: types.Message):
    await message.answer(f'Hi, {message.chat.username}. Just send /cat and you got some reward')


@dp.message_handler(commands='start')
async def reply2(message: types.Message):
    await message.answer(f'Hi, {message.chat.username} {emojize(":wink:")} Just send /cat and you got some reward')



#dp.register_message_handler(reply2, commands='start')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)