import requests
from telegram_token import token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("I'm echo bot")

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

if __name__ == "__main__":
    executor.start_polling(dp)
