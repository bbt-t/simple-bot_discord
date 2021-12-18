from discord import Member, utils
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


@bot.command('mute')
@commands.has_permissions(administrator=True)
async def mute_user(msg, member: Member, *, reason=None):
    mute_role = utils.get(msg.message.guild.roles, name='muted')
    await msg.channel.purge(limit=1)

    await member.edit(roles=())
    await member.add_roles(mute_role, reason=reason)
    await member.send(f'Ты получил мут на {msg.guild.name}')
    logger.warning(f'{member.mention} : was muted')


@bot.command('unmute')
@commands.has_permissions(administrator=True)
async def mute_user(msg, member: Member):
    mute_role = utils.get(msg.message.guild.roles, name='muted')
    role = utils.get(msg.message.guild.roles, name='стопка')

    await msg.channel.purge(limit=1)

    await member.remove_roles(mute_role)
    await member.add_roles(role)
    await member.send(f'Ты размучен на {msg.guild.name}')
    logger.warning(f'{member.mention} : was unmute')
