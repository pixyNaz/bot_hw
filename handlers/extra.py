from aiogram import Dispatcher, types
from  config import bot, dp


# @dp.message_handler()
async def echo(message: types.Message):
    try:
        number = int(message.text)
        result = number ** 2
        await bot.send_message(chat_id=message.from_user.id, text=result)
    except ValueError:
        await bot.send_message(chat_id=message.from_user.id, text=message.text)

    if message.text.startswith('!'):
        await message.pin()


def register_handler_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
