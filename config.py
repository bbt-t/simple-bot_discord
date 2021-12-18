from os import getenv
from zoneinfo import ZoneInfo
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()




TOKEN = getenv('TOKEN')
APPLICATION_ID = getenv('APPLICATION_ID')
SERVER_ID = getenv('SERVER_ID')
ADMIN_ROLE = getenv('ADMIN_ROLE')

settings: dict = {
    'token': TOKEN,
    'id': APPLICATION_ID,
    'prefix': '!'
}

forbidden_words = frozenset((
    'мат1', 'мат2', 'мат3'
))

time_now = datetime.now(ZoneInfo('Europe/Moscow'))
