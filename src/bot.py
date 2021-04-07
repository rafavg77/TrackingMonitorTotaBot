import os
import logging
import traceback
import json
import html
from configparser import ConfigParser
from  telegram import ReplyKeyboardMarkup, ParseMode, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext
from Utils.trackingMailAmericas import TrackApi
from Utils.sendToTelegram import sendPhoto

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'Utils/config/config.ini')
config = ConfigParser()
config.read(initfile)
token_bot = config.get('telegram_bot', 'telegram_token')
bad_permission = config.get('users', 'reply')
DOWNLOAD_PATH = config.get('base','base_dowload')


def isPermited(update, context):
    id = update.message.chat.id
    logger.info(id)
    PERMITED_USERS = config.get('users',"permited")
    if str(id) in PERMITED_USERS:
        permission = True
    else:
        permission = False
        update.message.reply_text(bad_permission)
        logger.warning("Warning id of user without permission: " + str(update.message.chat.id))
        logger.warning("Warning username of user without permission: "+ str(update.message.chat.username))
        logger.warning("Warning Gruop without permission: "+ str(update.message.chat.title))
        

    return permission 

def start(update, context):
    if isPermited(update, context):
        logger.info('I have received a /start command')
        update.message.reply_text("Hi Master, I'm here to server you!! /help")

def help(update, context):
    if isPermited(update, context):
        reply_keyboard = [['Ping', 'Tracking Status']]
        choice = update.message.reply_text(
            "Choose a Command to execute:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        print(choice)
        return choice

def ping(update, context):
    logger.info('I have received a /ping command')
    if isPermited(update, context):
        update.message.reply_text("Pong !!")

def reply(update, context):
    user_input = update.message.text
    chat_id=update.message.chat_id
    if isPermited(update, context):
        if user_input == "Tracking Status":
            #update.message.reply_text("Requesting last Status, wait a moment... ")
            getTrackingStatus(update, context,chat_id)
        elif user_input == "Ping":
            ping(update, context)

def getTrackingStatus(update, context,chat_id):
    try:
        status = TrackApi()
        lastStatus = status.accessTraking()
        logging.info("Sending: " + DOWNLOAD_PATH+lastStatus)
        print(open(DOWNLOAD_PATH+lastStatus,'rb'))
        #context.bot.send_photo(chat_id=chat_id,photo=open(DOWNLOAD_PATH+lastStatus,'rb'))
        send = sendPhoto(lastStatus,chat_id)
    except ValueError as err:
        logging.error(err)

def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )   

    # Finally, send the message
    context.bot.send_message(chat_id=bad_permission[0], text=message, parse_mode=ParseMode.HTML)


if __name__ == '__main__':

    updater = Updater(token=token_bot,use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Ping|Tracking Status)$'), reply))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()