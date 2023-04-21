from mailbox import Message

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from .import client_kb


class FSMAdminMentor(StatesGroup):
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdminMentor.name.set()
        await message.answer("Какой завут у ментора!?", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Пишите в личку!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["telegram_id"] = message.text
        data["username"] = message.text
        data["name"] = message.text
    await FSMAdminMentor.next()
    await message.answer("Какой напрвление?")


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["direction"] = message.text
    await FSMAdminMentor.next()
    await message.answer("Сколька лет ментору?")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пишите только число!")
    else:
        async with state.proxy() as data:
            data["age"] = message.text
        await FSMAdminMentor.next()
        await message.answer("В какой группе?")


async def load_group(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пишите только число!")
    else:
        async with state.proxy() as data:
            data["group"] = message.text
        await message.answer(
            f"{data['name']} {data['direction']} {data['age']} {data['group']}"
        )
        await FSMAdminMentor.next()
        await message.answer("Все верно?", reply_markup=client_kb.submit_markup)


async def submit_state(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.finish()
        await message.answer("Замечательно!")
        await message.answer("заново?", reply_markup=client_kb.submit_markup)
    elif message.text.lower() == "заново":
        await FSMAdminMentor.name.set()
        await message.answer("Как зовут у ментора!?")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Отменили!")


def register_handler_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_reg,Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdminMentor.name)
    dp.register_message_handler(load_direction, state=FSMAdminMentor.direction)
    dp.register_message_handler(load_age, state=FSMAdminMentor.age)
    dp.register_message_handler(load_group, state=FSMAdminMentor.group)
    dp.register_message_handler(submit_state, state=FSMAdminMentor.submit)
