from config import forbidden_words
from loader import bot, logger




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
            if user_warnings := db.select_warning(user_id=user.id) == 1:
                await msg.send('ЦЫЦ! читай правила чата! В следующий раз будет мут...')
            elif 1 < user_warnings <= 3:
                mute_role = utils.get(msg.guild.roles, name='muted')
                await user.edit(roles=())
                await user.add_roles(mute_role)
                await msg.send('АЙАЙАЙ! читай правила чата! x2')
            elif 3 < user_warnings <= 6:
                await user.kick(reason='Договорился -_-')
            else:
                await user.ban(reason='за грязный рот :С')
        except TypeError as err:
            logger.info(f'{repr(err)} : NoneType - not a single crime yet :)')
        finally:
            await msg.delete()
    await bot.process_commands(msg)
