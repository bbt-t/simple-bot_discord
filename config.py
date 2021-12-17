from os import getenv

from dotenv import load_dotenv
load_dotenv()




TOKEN = getenv('TOKEN')
APPLICATION_ID = getenv('APPLICATION_ID')
SERVER_ID = getenv('SERVER_ID')

settings = {
    'token': TOKEN,
    'id': APPLICATION_ID,
    'prefix': '!'
}

forbidden_words = (
    'мат1', 'мат2', 'мат3'
)