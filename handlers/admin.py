from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from config import bot, ADMINS
from database.bot_db import sql_command_all, sql_command_delete


async def ban(message: types.Message):
    if message.chat.type !='admin':
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


async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer('Ты не администратор!')
    else:
        users = await sql_command_all()
        for user in users:
            info = f"{user[3]} {user[4]} " \
                   f"{user[5]} {user[-1]}"
            info = info + f"\n\n@{user[2]}" if user[2] else info
            caption = info
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"DELETE {user[3]}",
                                     callback_data=f"delete {user[0]}"
                )
            )


async def complete_delete(call: types.CallbackQuery):
    user_id = call.data.replace("delete ", "")
    await sql_command_delete(user_id)
    await call.answer(text=f"Удалено запись с айди {user_id}",
                      show_alert=True)
    await call.message.delete()


async def admins_command(message: Message) -> Message:
    chat_id = message.chat.id
    admins = await message.bot.get_chat_administrators(chat_id)
    text = ''
    for admin in admins:
        text += f'@{admin.user.username} '
    return await message.answer(text, disable_notification=True)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(
        complete_delete,
         lambda call: call.data and call.data.startswith("delete"))


