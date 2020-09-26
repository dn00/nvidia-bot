
from chromedriver_py import binary_path  # this will get you the path variable
from utils.logger import log
import webbrowser
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from utils.selenium_utils import options, enable_headless, wait_for_element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CHECK_URL = "https://www.newegg.com/p/pl?N=100007709%20601357282%20601321572"
CHECK_URL = "https://www.newegg.com/p/pl?N=100007709%20601357282"
# CHECK_URL = "https://www.newegg.com/p/pl?d=2070"
ATC_URL = "https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList="
CART_URL = "https://secure.newegg.com/Shopping/ShoppingCart.aspx?Submit=view"
ATC_TEXT = "add to cart"

List = {'N82E16814126453', 'N82E16814487518', 'N82E16814126452', 'N82E16814487519', 'N82E16814487521'}

class NeweggChecker:
    def __init__(self, headless, delay):
        if headless:
            enable_headless()
        self.driver = webdriver.Chrome(executable_path=binary_path, options=options)
        self.delay = delay

    def check(self):
        self.driver.get(CHECK_URL)
        EC.presence_of_element_located((By.CLASS_NAME, "page-footer"))

        while True:
            item_containors = self.driver.find_elements(By.CLASS_NAME, "item-container")
            productIds = []
            for item in item_containors:
                log.info(item.find_element(By.CLASS_NAME, "item-title"))
                if (self.is_atc(item)):
                    title_a = item.find_element(By.CLASS_NAME, "item-title")
                    productId = item.find_element(By.CLASS_NAME, "item-title").get_attribute("href").rpartition('/')[-1]
                    log.info(f"{title_a.text} - {productId} IN STOCK")
                    productIds.append(productId)
                    
            log.info(productIds)
            topPid = [x for x in List if x in productIds]
            if (len(topPid) > 0):
                webbrowser.open(f'{ATC_URL}{topPid[0]}')
                time.sleep(0.5)
                webbrowser.open(f'{CART_URL}')
                return
            time.sleep(self.delay)
            self.driver.refresh()


    def is_atc(self, item):
        try:
            button = item.find_element(By.CSS_SELECTOR, "button")
            if button.text.lower() == ATC_TEXT:
                return True
            return False
        except Exception:
            print(Exception)
            return False
