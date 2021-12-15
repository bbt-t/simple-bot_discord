from config import settings
from loader import bot, logger




@bot.event
async def on_ready():
    logger.warning('bot started')


@bot.command('info')
async def info_bot(message):
    user = message.message.author
    await message.send(f'Привет, {user.mention}\n'
                       f'я тут главый смотрящий Бот!:)\n'
                       f'Этот канал ... в нём ты надёшь ... \n'
                       f'Для дополнительной справки -> <...>\n'
                       f'Общий спискок моих команд -> <...>')


@bot.command('auth')
async def authorization_request(call, *, msg):
    await call.send(f'Your message: {msg}')


@bot.event
async def on_message(message):
    user = message.author.mention
    match message.content.lower():
        case 'привет':
            await message.channel.send(f'Привет! :)')
        case 'МАТ' | 'МАТ' | 'МАТ' as forbidden_words:
            logger.warning(f'Пользователь {user}, пишет зарещённые правилами сообщения: {forbidden_words}')
            await message.delete()


if __name__ == '__main__':
    bot.run(settings['token'])