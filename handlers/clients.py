from datetime import datetime, timedelta
from parserr.news import parser
from aiogram import Dispatcher, types
from config import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from send_video import send_video
from .client_kb import start_markup
from database.bot_db import sql_command_random, sql_command_all_users, sql_command_insert_user
from .utils import get_ids_from_users


# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    users = await sql_command_all_users()
    ids = get_ids_from_users(users)
    if message.from_user.id not in ids:
        await sql_command_all_users(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name
        )

    await bot.send_message(message.from_user.id, f"Привет подруга {message.from_user.full_name}!")


async def help_command(message: types.Message):
    await message.reply('I need help.')


async def photos(message: types.Message):
    photo = open('media/mem2.jpeg', 'rb')
    await message.answer_photo(photo, caption='Не беси меня!', reply_markup=start_markup)


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


async def get_random_mentor(message: types.Message):
    random_user = await sql_command_random()
    info = f"{random_user[3]} {random_user[4]} " \
           f"{random_user[5]} {random_user[-1]}"
    info = info + f"\n\n@{random_user[2]}" if random_user[2] else info
    caption = info


async def get_news_data(message: types.Message):
    await message.delete()
    current_date: datetime = datetime.now()
    date_list = [current_date - timedelta(days=i) for i in range(6)]
    markup = InlineKeyboardMarkup(row_width=1)
    for date in date_list:
        markup.add(
            InlineKeyboardButton(
                date.strftime("%d.%m.%Y"),
                callback_data=f"date {date.strftime('%Y-%m-%d')}"
            )
        )
    await message.answer("Выберите дату: ", reply_markup=markup)


async def send_news(call: types.CallbackQuery):
    date = call.data.replace("date ", "")
    news = parser(year=date[:4], month=date[5:7], day=date[-2:])
    for i in news[:6]:
        await call.message.answer(
            f"{i['url']}\n"
            f"{i['title']} {i['data']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(photos, commands=['photo'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text="quiz_1_button")
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(get_random_mentor, commands=['get'])
    dp.register_message_handler(get_news_data, commands=['news'])
    dp.register_message_handler(send_video, commands=["video"])
    dp.register_callback_query_handler(
        send_news,
        lambda call: call.data and call.data.startswith("date ")
    )
