import os
import logging
import requests
from configparser import ConfigParser

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config/config.ini')
config = ConfigParser()
config.read(initfile)

BOT_TOKEN = config.get('telegram_bot','telegram_token')
BOT_CHAT = config.get('telegram_bot','telegram_chat_id')
BOT_URL = config.get('telegram_bot','telegram_url')
TRACKING_URL = config.get('mail_americas','mail_americas_url')
DRIVER_PATH = config.get('base','driver_path')
DOWNLOAD_PATH = config.get('base','base_dowload')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def sendPhoto(file,chat_id):
    try:
        if chat_id == '':
            BOT_CHAT_ID = BOT_CHAT
        else:
            BOT_CHAT_ID = chat_id
        logging.info("[+] Sending Telegram Photo ...")
        logging.info(DOWNLOAD_PATH + file)
        PARAMS = {'chat_id' : BOT_CHAT_ID, 'caption':'Este es el status al día de hoy'}
        files = { 'photo' : open(DOWNLOAD_PATH + file,'rb') } 
        r = requests.post(BOT_URL,PARAMS,files=files)
    except ValueError as err:
        logging.error(err)