from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('TOKEN')
APPLICATION_ID = getenv('APPLICATION_ID')

settings = {
    'token': TOKEN,
    'id': APPLICATION_ID,
    'prefix': '!'
}