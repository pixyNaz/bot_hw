from aiogram import Dispatcher, types
from aiogram.types import Message

from config import bot, ADMINS


async def ban(message: types.Message):
    if message.chat.type !='private':
        if message.from_user.id not in ADMINS:
            await message.answer('Ты не администратор!')
        elif not message.reply_to_message:
            await message.answer('Команда должна быть ответом на сообщение!')
        else:
            await bot.kick_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id
            )
        await message.answer(
            f'{message.from_user.first_name} администратор удалил'
            f'{message.reply_to_message.from_user.full_name}'
        )
    else:
        await message.answer('Пиши в группе!')


async def admins_command(message: Message) -> Message:
    chat_id = message.chat.id
    admins = await message.bot.get_chat_administrators(chat_id)
    text = ''
    for admin in admins:
        text += f'@{admin.user.username} '
    return await message.answer(text, disable_notification=True)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
