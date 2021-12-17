from sqlite3 import Error as sqlite_Error

from handlers import all_handlers
from config import settings
from loader import bot, logger, db




@bot.event
async def on_ready():
    try:
        db.del_table()
        db.create_table_users()
    except sqlite_Error:
        logger.warning('Error DB on start bot!')
    logger.warning('bot started')


if __name__ == '__main__':
    bot.run(settings['token'])