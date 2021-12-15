from discord.ext import commands

from loguru import logger
from config import settings




bot = commands.Bot(command_prefix=settings['prefix'])

logger.add(
    'logging-bot-discord.log',
    format='{time} {level} {message}',
    level='WARNING',
    rotation='00:00',
    compression='gz',
    )
