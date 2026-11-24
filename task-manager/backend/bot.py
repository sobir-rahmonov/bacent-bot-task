
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)

from config import BOT_TOKEN, WEBAPP_URL


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_keyboard():

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🚀 Open Task Manager",
                    web_app=WebAppInfo(
                        url=WEBAPP_URL
                    )
                )
            ]
        ],
        resize_keyboard=True
    )

    return keyboard


@dp.message(CommandStart())
async def start_handler(message: Message):

    user = message.from_user

    await message.answer(
        f"Assalomu alaykum, {user.first_name}! 👋\n\n"
        "Task Manager ilovasiga xush kelibsiz.\n\n"
        "Kundalik vazifalaringizni boshqarish uchun "
        "quyidagi tugmani bosing.",
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("help"))
async def help_handler(message: Message):

    await message.answer(
        "Task Manager bot yordam bo'limi.\n\n"
        "/start - Ilovani ochish\n"
        "/help - Yordam"
    )
