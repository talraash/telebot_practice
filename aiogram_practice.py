from aiogram import Bot, Dispatcher, executor, types
from telegram_token import token
import aiohttp
from aiogram.utils.emoji import emojize
from bs4 import BeautifulSoup


bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def cat():
    async with aiohttp.ClientSession() as cat_session:
        async with cat_session.get("http://aws.random.cat/meow") as respond:
            file = await respond.json()
            return file['file']



@dp.message_handler(commands='cat')
async def reply(message: types.Message):
    file = await cat()
    await bot.send_photo(message.chat.id, file)


@dp.message_handler(commands='help')
async def reply2(message: types.Message):
    await message.answer(f'Hi, {message.chat.full_name}. Just send /cat and you got some reward')


@dp.message_handler(commands='start')
async def reply2(message: types.Message):
    await message.answer(f'Hi, {message.chat.username} {emojize(":wink:")} Just send /cat and you got some reward')

url = []
@dp.message_handler()
async def get_fantlab_content(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://fantlab.ru/searchmain?searchstr=' + message.text) as respond:
            text = await respond.read()
    soup = BeautifulSoup(text.decode('utf-8'), 'lxml')
    info = soup.find(class_='search-block works')
    rathings = info.select('big', limit=3)
    autor = info.find_all(class_='autor', limit=3)
    title = info.find_all(class_='title', limit=3)
    for i in title:
        t = str(i.find('a'))
        url.append("fantlab.ru" + t[t.find('/'):t.rfind('"')])
    for i in range(3):
        print(f'Рейтинг :{rathings[i]} \n Автор :{autor[i]},\n Произведение :{title[i]} \n Ссылка: {url[i]}')
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
