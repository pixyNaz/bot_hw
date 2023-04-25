import datetime
from sched import scheduler

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.bot_db import sql_command_all_users
from config import bot


async def reminder(bot: Bot):
    users = await sql_command_all_users()
    for user in users:
        await bot.send_message(user[0], f"Good day {user[-1]} You have a Appointment on Monday to dentist!")


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")

    scheduler.add_job(
        reminder,
        kwargs={"bot": bot},
        trigger=CronTrigger(
            hour=20,
            start_date=datetime.datetime.now()
        )
    )
    scheduler.start()


