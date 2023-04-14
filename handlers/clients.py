from aiogram import Dispatcher, types
from  config import bot, dp
from  aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"Привет подруга {message.from_user.full_name}!")


async def help_command(message: types.Message):
    await message.reply('I need help.')


# @dp.message_handler(commands=['photo'])
async def photos(message: types.Message):
    photo = open('media/mem2.jpeg', 'rb')
    await message.answer_photo(photo, caption='Не беси меня!')


# @dp.message_handler(commands=['quiz'])
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


async def quiz_2(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_2 = InlineKeyboardButton("NEXT", callback_data="quiz_2_button")
    markup.add(button_2)
    question = "Какой герой мультфильма живет в ананасе под водой?"
    answer = [
        "Камбала",
        "Немо",
        "Губка Боб Квадратные Штаны",
        "Рик и Морти",
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="",
        open_period=15,
        reply_markup=markup
    )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(photos, commands=['photo'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text="quiz_1_button")
    dp.register_message_handler(help_command, commands=['help'])

