from discord import Embed, Color, errors, utils
from discord.ext import commands

from config import forbidden_words, time_now
from loader import bot, logger, db




@bot.event
async def on_message(msg):
    """
    Warning -> kick -> ban.
    """
    user = msg.author

    if any(''.join(ch for ch in let if ch.isalnum) in forbidden_words for let in msg.content.lower().split()):
        logger.warning(f'Пользователь {user.id=}, пишет запрещённые правилами сообщения!')
        db.add_warnings(user_id=user.id)

        try:
            if user_warnings := db.select_warning(user_id=user.id) <= 3:
                mute_role = utils.get(msg.guild.roles, name='muted')
                await user.edit(roles=())
                await user.add_roles(mute_role)
                await msg.send('АЙАЙАЙ! читай правила чата!')
            elif 3 < user_warnings <= 6:
                await user.kick(reason='Договорился -_-')
            else:
                await user.ban(reason='за грязный рот :С')
        except TypeError as err:
            logger.info(f'{repr(err)} : NoneType - not a single crime yet :)')
        finally:
            await msg.delete()
    await bot.process_commands(msg)



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


@bot.command('подчистить')
@commands.has_permissions(administrator=True)
async def deleting_messages(msg, amt=2):
    """
    Delete message
    :param amt: how much message to delete
    """
    await msg.channel.purge(limit=amt)


@bot.command('auth')
async def authorization_request(call, *, msg):
    await call.send(f'Your message: {msg}')
