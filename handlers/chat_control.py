from datetime import timedelta

from discord import utils

from config import forbidden_words, time_now
from loader import bot, logger, scheduler, db
from utils.forgiveness_of_the_offender import unmute_user


@bot.event
async def on_message(msg):
    """
    Warning -> kick -> ban.
    """
    user = msg.author

    if any(''.join(ch for ch in let if ch.isalnum) in forbidden_words for let in msg.content.lower().split()):
        logger.warning(f'Пользователь {user.id=}, пишет запрещённые правилами сообщения!')

        try:
            db.add_warnings(user_id=user.id)
            user_warnings = db.select_warning(user_id=user.id)[0]

            if user_warnings == 1:
                await user.send('ЦЫЦ! читай правила чата! В следующий раз будет мут...')
            elif 1 < user_warnings <= 3:
                for guild in bot.guilds:
                    mute_role = utils.get(guild.roles, name='muted')
                await user.edit(roles=())
                await user.add_roles(mute_role)
                await user.send('АЙАЙАЙ! читай правила чата! x2')
                date = time_now + timedelta(hours=3)
                scheduler.add_job(
                    unmute_user, 'date', id=f'{user.id}_mute',
                    run_date=date.strftime('%Y-%m-%d %H:%M:%S'),
                    timezone='Europe/Moscow',
                    args=(user,)
                )
            elif 3 < user_warnings <= 6:
                await user.kick(reason='Договорился -_-')
            if user_warnings > 6:
                await user.ban(reason='за грязный рот :С')
        except TypeError as err:
            logger.info(f'{repr(err)} : NoneType - not a single crime yet :)')
        finally:
            await msg.delete()

    await bot.process_commands(msg)
