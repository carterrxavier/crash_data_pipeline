import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
print(selenium.__version__)

options = webdriver.ChromeOptions()
dir_path = os.path.dirname(os.path.realpath('chromedriver'))
chromedriver = dir_path + '/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver
pattern = r"https://app\.myaccident\.org/accident/\d+$"


def scrape_data(start_date, end_date, city):



        url = 'https://app.myaccident.org/results?startDate=2024-02-01&endDate=2024-02-18&lat=29.432050423986603&lng=-98.48402088539248&radius=20000'

        driver = webdriver.Chrome(options=options)     
        driver.get(url)

        #wait for class result to load
        links = []

        ui.WebDriverWait(driver, timeout=100).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result')))
        #grab href tags to grab all the links needed to scrape for the next phase
        containers = driver.find_elements(By.TAG_NAME,'a')

        for con in containers:
                if re.match(pattern,str(con.get_attribute('href'))):
                        links.append(con.get_attribute('href'))
        driver.close()

        return links