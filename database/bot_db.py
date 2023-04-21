import random
import sqlite3
from typing import List, Any


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("Вы успешно подключили на база данных!")

    db.execute(
        'CREATE TABLE  IF NOT EXISTS mentor '
        '(id INTEGER PRIMARY KEY AUTOINCREMENT , '
        ' telegram_id INTEGER UNIQUE, '
        'username VARCHAR(50),'
        'name VARCHAR(50),'
        'direction VARCHAR(50),'
        'age INTEGER,'
        'gruop INTEGER)'

    )
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO mentor VALUES"
                       "(null, ?, ?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random():
    users: list[Any] = cursor.execute("SELECT * FROM mentor").fetchall()
    random_user = random.choice(users)
    return random_user


async def sql_command_all():
    return cursor.execute("SELECT * FROM manter").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM mentor WHERE id == ?", (id,))
    db.commit()