import os
import time
import logging
import requests
from configparser import ConfigParser
from warnings import filterwarnings
from selenium import webdriver
from Screenshot import Screenshot_Clipping 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config/config.ini')
config = ConfigParser()
config.read(initfile)
ob=Screenshot_Clipping.Screenshot() 

BOT_TOKEN = config.get('telegram_bot','telegram_token')
BOT_CHAT = config.get('telegram_bot','telegram_chat_id')
BOT_URL = config.get('telegram_bot','telegram_url')
TRACKING_URL = config.get('mail_americas','mail_americas_url')
DRIVER_PATH = config.get('base','driver_path')
DOWNLOAD_PATH = config.get('base','base_dowload')
CONFIG_HEADLESS = config.get('base','config_headless')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TrackApi:

    def accessTraking(self):
        try:
            logging.info("Running Tracking Script ... ")
            options = Options()
            options.headless = CONFIG_HEADLESS
            options.add_argument("--window-size=1920,1200")
            profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
                "download.default_directory": DOWNLOAD_PATH , "download.extensions_to_open": "applications/pdf"}
            options.add_experimental_option("prefs", profile)
            driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
            driver.get(TRACKING_URL)
            logging.info("Opening " + TRACKING_URL)

            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-aliexpress"]')))
            closeModal = driver.find_element_by_xpath('//*[@id="modal-aliexpress"]/div/div/div[1]/button')
            closeModal.click()
            time.sleep(2)
            name_file = time.strftime("%Y%m%d-%H%M%S") + ".png"
            img_url=ob.full_Screenshot(driver, save_path=DOWNLOAD_PATH, image_name=name_file)
            driver.quit() 
        except ValueError as err:
            logging.error("Error in accessTraking")
            logging.error(err)
            driver.quit()
        return name_file

    #def getTrackingStatus(self):
    #    file = accessTraking(driver)
    #    driver.quit()
    #    return file
