from sqlite3 import Error as sqlite_Error

import handlers
from config import settings
from loader import bot, logger, db, scheduler




@bot.event
async def on_ready():
    try:
        db.del_table()
        db.create_table_users()
    except sqlite_Error:
        logger.warning('Error DB on start bot!')
    logger.warning('bot started')
    scheduler.print_jobs()


if __name__ == '__main__':
    scheduler.start()
    bot.run(settings['token'])