from aiogram.utils import executor
import logging

from config import dp
from handlers import clients, extra, callback, admin, fsm_anketa

clients.register_handlers_client(dp)
callback.register_handler_callback(dp)
admin.register_handler_admin(dp)
fsm_anketa.register_handler_fsm(dp)


extra.register_handler_extra(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
