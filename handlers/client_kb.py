from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2

)

start_button = KeyboardButton("Start")
quiz_button = KeyboardButton("Quiz")
help_button = KeyboardButton("Help")
remove_button = KeyboardButton("Remove")

start_markup.add(start_button, quiz_button, help_button, remove_button)

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
).add(
    KeyboardButton("ОТМЕНА")
)

submit_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
).add(
    KeyboardButton("ДА"),
    KeyboardButton("ЗАНОВО")
)