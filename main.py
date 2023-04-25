from aiogram.utils import executor
import logging

from config import dp, ADMINS, bot
from handlers import clients, extra, callback, admin, fsm_anketa, scheduler
from database.bot_db import sql_create

clients.register_handlers_client(dp)
callback.register_handler_callback(dp)
admin.register_handler_admin(dp)
fsm_anketa.register_handler_fsm(dp)

extra.register_handler_extra(dp)


async def mentordb(dp):
    await scheduler.set_scheduler()
    sql_create()
    await bot.send_message(ADMINS[0], "Добрый день, я здесь чтобы вам помогат!")


async def shutdown(dp):
    await bot.send_message(ADMINS[0], "До скорого!")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=mentordb, on_shutdown=shutdown)
