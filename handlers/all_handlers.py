from discord import Embed, Color, errors
from config import forbidden_words
from loader import bot, logger, db


@bot.command('info')
async def info_bot(message):
    """
    Отправляет сообщеие в ЛС
    :param message: сообщение
    :return: сообщение в ЛС написавшему команду
    """
    user = message.message.author
    await user.send(f'Привет, {user.id}\n'
                    f'я тут главый смотрящий Бот!:)\n'
                    f'Этот канал ... в нём ты надёшь ... \n'
                    f'Для дополнительной справки -> <...>\n'
                    f'Общий спискок моих команд -> <...>')


@bot.command('auth')
async def authorization_request(call, *, msg):
    await call.send(f'Your message: {msg}')


@bot.event
async def on_message(message):
    """
    Предупреждение -> бан за мат.
    """
    user_id = message.author.id

    if any(''.join(ch for ch in let if ch.isalnum) in forbidden_words for let in message.content.lower().split()):
        logger.warning(f'Пользователь {user_id=}, пишет запрещённые правилами сообщения!')
        await message.delete()

        db.add_warnings(user_id=user_id)
        if db.select_warning(user_id=user_id) > 3:
            await message.author.ban(reason='за грязный рот :С')

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    db.add_user(user_id=member.id, name=member.name)
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
