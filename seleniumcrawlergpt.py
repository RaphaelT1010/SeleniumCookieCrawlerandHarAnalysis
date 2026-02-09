from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
import json
import pandas as pd
import time

# Constants
BROWSERMOB_PATH = r"C:\Users\Raph\Desktop\152A\Project2\bin\browsermob-proxy.bat"
PAGE_LOAD_TIMEOUT = 180
MAX_WEBSITES = 1000

# Function to initialize WebDriver with options
def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    return driver

# Create a browsermob server instance
server = Server(BROWSERMOB_PATH)
server.start()
proxy = server.create_proxy(params=dict(trustAllServers=True))

# Create a new chromedriver instance
driver = initialize_driver()

try:
    df = pd.read_csv(r"C:\Users\Raph\Desktop\152A\Project2\editedtop-1m.csv")

    for websitename in df.iloc[:MAX_WEBSITES]['name']:
        # do crawling
        print("Gathering cookies for website:", websitename)
        proxy.new_har(websitename, options={'captureCookies': True, 'captureHeaders': True, 'captureContent': False})
        starttime = time.time()

        try:
            driver.get("http://" + websitename)
            with open(websitename + ".har", 'w') as f:
                f.write(json.dumps(proxy.har))

        except (WebDriverException, TimeoutException):
            # Restart the driver if an exception occurs
            driver.quit()
            driver = initialize_driver()
            continue

        if time.time() - starttime >= PAGE_LOAD_TIMEOUT:
            # Restart the driver if it takes too long
            driver.quit()
            driver = initialize_driver()

finally:
    # Stop server and exit
    server.stop()
    driver.quit()