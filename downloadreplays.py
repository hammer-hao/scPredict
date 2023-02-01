from selenium import webdriver
from selenium.webdriver import Chrome
import time
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

options=Options()
prefs = {"download.default_directory" : "replays_raw"}
options.add_experimental_option("prefs",prefs)

drive_path="C:/Users/hammerhao/OneDrive/Desktop/chromedriver_win32/chromedriver.exe"
driver=Chrome(drive_path, chrome_options=options)

link = "https://sc2rep.ru/index.php?gt=1&matchup1x1=5&only_pro=0&page=0"
driver.get(link)

for i in tqdm(range(86)):
    pageno=20*i
    link="https://sc2rep.ru/index.php?gt=1&matchup1x1=5&only_pro=0&page="+str(pageno)
    driver.get(link)
    for i in range(20):
        element_id= 2*i+3
        css_selector=('#quotes > table > tbody > tr > td:nth-child(2) > table:nth-child(5) > tbody > tr:nth-child('+str(element_id)+') > td:nth-child(10) > a > img')
        thisdownloadbutton=driver.find_element('css selector', css_selector)
        thisdownloadbutton.click()
        time.sleep(1)

driver.close()