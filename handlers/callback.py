from aiogram import Dispatcher, types
from config import bot, dp


async def quiz_3(call: types.CallbackQuery):
    question = "Какой город является столицей Канады?"
    answer = [
        "Оттава",
        "Торонто",
        "Квебек",
        "Калгари",
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation="",
        open_period=15,
    )


def register_handler_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_3, text="quiz_2_button")
