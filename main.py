from handlers import all_handlers
from config import settings
from loader import bot, logger, db




@bot.event
async def on_ready():
    db.del_table()
    db.create_table_users()
    logger.warning('bot started')


if __name__ == '__main__':
    bot.run(settings['token'])