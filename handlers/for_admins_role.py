from discord import Member
from discord.ext import commands

from loader import bot, logger




@bot.command('подчистить')
@commands.has_permissions(administrator=True)
async def deleting_messages(msg, amt=2):
    """
    Delete message
    :param amt: how much message to delete
    """
    await msg.channel.purge(limit=amt)


@bot.command('kick')
@commands.has_permissions(administrator=True)
async def kick_user(msg, member: Member, *, reason=None):
    await msg.channel.purge(limit=1)
    await member.kick(reason=reason)
    await msg.send(f'{member.mention} was kicked')
    logger.warning(f'{member.mention} : was kicked')


@bot.command('ban')
@commands.has_permissions(administrator=True)
async def ban_user(msg, member: Member, *, reason=None):
    await msg.channel.purge(limit=1)
    await member.ban(reason=reason)
    await msg.send(f'{member.mention} was banned')
    logger.warning(f'{member.mention} : was banned')




