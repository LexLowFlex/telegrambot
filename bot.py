
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = "8074284657:AAE9cKvdl_rOGmCdMSK5cRcx-6HvY3ZkgVg"  # Твой токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = KeyboardButton(
        text="🎰 Играть",
        web_app=WebAppInfo(url="https://telegram-spin-app.vercel.app/")
    )
    keyboard.add(web_app_button)
    await message.answer("Нажми кнопку ниже, чтобы сыграть 🎰", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp)
