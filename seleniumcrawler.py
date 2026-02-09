from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
import json
import pandas as pd
import signal
import time

# create a browsermob server instance
server = Server(r"C:\Users\rapha\Desktop\152A\Project2\bin\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy(params=dict(trustAllServers=True))

# create a new chromedriver instance
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('log-level=3')
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(180)  # Will wait 3 minutes at most to get cookies. If it takes too long, bad website or enormous amount of headers

df = pd.read_csv(r"C:\Users\rapha\Desktop\152A\Project2\editedtop-1m.csv")

for websitename in df.iloc[:1000]['name']:
    # do crawling
    print("Gathering cookies for website: " + websitename)
    proxy.new_har(websitename,options={'captureCookies': True,'captureHeaders' : True, 'captureContent': False})
    starttime = time.time()
    
    try:
        driver.get("http://" + websitename)
        with open(websitename + ".har", 'w') as f:
            f.write(json.dumps(proxy.har))
           
        
    #If we fail to read headers after three minutes, quit the instasnce and start a new one.
    except (WebDriverException,TimeoutException) as e:
        driver.quit() #Restart chrome instance
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(180)  # Will wait 3 minutes at most to get cookies. If it takes too long, bad website or enormous amount of headers
        continue

    if time.time() - starttime >= 180: #Sometimes, be able to get website (not throwing webdriverexception or timeoutexception) But for other reasons, headers won't be read (cookie cache may be full)
        driver.quit()
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(180)  # Will wait 3 minutes at most to get cookies. If it takes too long, bad website or enormous amount of headers
        continue

    #If passes everything, make a new driver (ensures fresh resources)
    driver.quit()
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(180)  # Will wait 3 minutes at most to get cookies. If it takes too long, bad website or enormous amount of headers


# stop server and exit
server.stop()
driver.quit()