from aiogram import types, Dispatcher
from config import bot


async def send_video(message: types.Message):
    video = open("/media/video.mp4", "rb")
    await bot.send_video(message.chat.id, video=video)


def register_handlers_send_video(dp: Dispatcher):
    dp.register_message_handler(send_video(), commands=["video"])


