from discord.ext import commands

from config import settings

bot = commands.Bot(command_prefix=settings['prefix'])


@bot.command()
async def call_bot(message):
    user = message.message.author
    await message.send(f'Hello!, {user.mention}!')


if __name__ == '__main__':
    bot.run(settings['token'])