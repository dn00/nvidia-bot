
from chromedriver_py import binary_path  # this will get you the path variable
from utils.logger import log
import webbrowser
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from utils.selenium_utils import options, enable_headless, wait_for_element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.page_load_strategy = "eager"
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


# CHECK_URL = "https://www.newegg.com/p/pl?N=100007709%20601357282%20601321572"
CHECK_URL = "https://www.newegg.com/p/pl?N=100007709%20601357282"
# CHECK_URL = "https://www.newegg.com/p/pl?d=2070"
ATC_URL = "https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList="
CART_URL = "https://secure.newegg.com/Shopping/ShoppingCart.aspx?Submit=view"
ATC_TEXT_LOWERCASE = "add to cart"
AYH_TEXT_LOWERCASE = "are you human?"

List = {'N82E16814126453', 'N82E16814487518', 'N82E16814137597', 'N82E16814126454', 'N82E16814487526', 'N82E16814126452', 'N82E16814487519', 'N82E16814487521'}

class NeweggChecker:
    def __init__(self, headless, delay):
        if headless:
            enable_headless()
        self.driver = webdriver.Chrome(executable_path=binary_path, options=options)
        self.delay = delay
        self.basePageTitle = ""

    def check(self):
        self.driver.get(CHECK_URL)
        EC.presence_of_element_located((By.CLASS_NAME, "page-footer"))
        self.basePageTitle = self.driver.title

        while True:
            log.info(self.driver.title)
            while self.driver.title != self.basePageTitle:
                log.info(self.driver.title)
                self.wait_enter_captcha()

            item_containors = self.driver.find_elements(By.CLASS_NAME, "item-container")
            log.info(f'{len(item_containors)} items found. Checking stock...')
            productIds = []
            for item in item_containors:
                # log.info(item.find_element(By.CLASS_NAME, "item-title"))
                if (self.is_atc(item)):
                    # title_a = item.find_element(By.CLASS_NAME, "item-title")
                    productId = item.find_element(By.CLASS_NAME, "item-title").get_attribute("href").rpartition('/')[-1]
                    productIds.append(productId)
                     
            log.info(productIds)
            topPid = [x for x in List if x in productIds]
            if (len(topPid) > 0):
                webbrowser.open("https://www.youtube.com/watch?v=GWXLPu8Ky9k")
                webbrowser.open(f'{ATC_URL}{topPid[0]}')
                time.sleep(0.5)
                webbrowser.open(f'{CART_URL}')
                return

            time.sleep(random.randint(self.delay, self.delay + 4))
            self.driver.refresh()


    def wait_enter_captcha(self):
        time.sleep(self.delay)
        log.info("Please enter captcha")

    def is_atc(self, item):
        try:
            button = item.find_element(By.CSS_SELECTOR, "button")
            if button.text.lower() == ATC_TEXT_LOWERCASE:
                return True
            return False
        except Exception:
            return False
