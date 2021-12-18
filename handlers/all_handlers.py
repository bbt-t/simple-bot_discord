from discord import Embed, Color, errors, utils
from discord.ext import commands

from config import time_now
from loader import bot, logger, db




@bot.event
async def on_member_join(member):
    """
    Registration of a new user in the DB.
    :param member: user-object
    :return: greeting to PM
    """
    db.add_user(user_id=member.id, name=member.name, reg_time=time_now.date())
    await member.send(embed=Embed(description=f'Привееет {member.name}! Рад тебя видеть!\n'
                                              f'На этом сервере я тебе буду помогать, пиши ``!info`` чтобы посмотреть мои возможности :)',
                                  color=Color.green()))


@bot.event
async def on_member_remove(member):
    try:
        await member.send(embed=Embed(description=f"Ты чегоо? :( Если у тебя возникли проблемы или другая "
                                                  f"причина почему ты нас покинул(а), то напиши нам! мы "
                                                  f"обязательно поможем/исправим!",
                                      color=Color.green()))
    except errors.Forbidden:
        logger.warning(f'{member.id=} : Cannot send messages to this user')


@bot.command('info')
async def info_bot(msg):
    """
    Отправляет сообщеие в ЛС, удаляет сообщение с командой.
    :param msg: сообщение
    :return: сообщение в ЛС написавшему команду
    """
    user = msg.message.author
    await user.send(f'Привет, {user.id}\n'
                    f'я тут главый смотрящий Бот!:)\n'
                    f'Этот канал ... в нём ты надёшь ... \n'
                    f'Для дополнительной справки -> <...>\n'
                    f'Общий спискок моих команд -> <...>')
    await msg.channel.purge(limit=1)


@bot.command('auth')
async def authorization_request(call, *, msg):
    await call.send(f'Your message: {msg}')
