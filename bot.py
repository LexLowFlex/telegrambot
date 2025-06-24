import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

API_TOKEN = '8148642069:AAFqos5HOo3Op_tNudRvIOFNqUeMbjjVaa0'
WEB_APP_URL = 'https://v0-new-project-3o4vvda4eqi.vercel.app/'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

scheduler = AsyncIOScheduler()
user_ids = set()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_ids.add(message.from_user.id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = KeyboardButton(
        text=" Играть",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    keyboard.add(web_app_button)

    await message.answer("Добро пожаловать! Нажми кнопку ниже, чтобы испытать удачу 🎯", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    user_ids.add(message.from_user.id)

async def send_reminder():
    if not user_ids:
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Забери выигрыш!", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, "🔔 Ты забыл забрать свой выигрыш! Жми ниже 👇", reply_markup=keyboard)
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение {user_id}: {e}")

async def on_startup(dp):
    scheduler.start()
    scheduler.add_job(send_reminder, 'interval', hours=2)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
