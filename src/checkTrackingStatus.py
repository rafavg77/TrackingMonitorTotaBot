from Utils.trackingMailAmericas import TrackApi
from Utils.sendToTelegram import sendPhoto
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

status = TrackApi()
lastStatus = status.accessTraking()
send = sendPhoto(lastStatus)