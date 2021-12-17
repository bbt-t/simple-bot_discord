import discord
from discord.ext import commands

from loguru import logger
from config import settings
from utils.db.sqlite import Database




bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())

db = Database()

logger.add(
    'logging-bot-discord.log',
    format='{time} {level} {message}',
    level='WARNING',
    rotation='00:00',
    compression='gz',
    )
