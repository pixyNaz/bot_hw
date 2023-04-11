import numbers
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from decouple import config
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = config("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"Привет подруга {message.from_user.full_name}!")
    await bot.send_photo(message.from_user.id,

                         f'https://i.pinimg.com/originals/fb/47/c1/fb47c13036491018852a4e4493c1c757.gif')


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="quiz_1_button")
    markup.add(button_1)
    question = "Самый большой вулкан Солнечной системы называется «Гора Олимп». Где он находится?"
    answer = [
        "Юпитер",
        "Земля",
        "Венера",
        "Марс",
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        open_period=15,
        reply_markup=markup
    )


@dp.callback_query_handler(text="quiz_1_button")
async def quiz_2(call: types.CallbackQuery):
    question = "Какой герой мультфильма живет в ананасе под водой?"
    answer = [
        "Камбала",
        "Немо",
        "Губка Боб Квадратные Штаны",
        "Рик и Морти",
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="",
        open_period=15,
    )


@dp.message_handler()
async def echo(message: types.Message):
    try:
        number = int(message.text)
        result = number ** 2
        await bot.send_message(chat_id=message.from_user.id, text=result)
    except ValueError:
        await bot.send_message(chat_id=message.from_user.id, text=message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
