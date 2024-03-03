import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
from aquire2 import get_page_data
from cities import check_city_support
from store_to_gcs import store_to_cloud


city = 'san antonio'
state = 'texas'
start_date = '2023-5-01'
end_date = '2023-5-14'


options = webdriver.ChromeOptions()
dir_path = os.path.dirname(os.path.realpath('chromedriver'))
chromedriver = dir_path + '/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
pattern = r"https://app\.myaccident\.org/accident/\d+$"

        
def scrape_data(start_date, end_date, city,state):  

        lat_long = check_city_support(city,state)

        if lat_long != None:
                url = f'https://app.myaccident.org/results?startDate={start_date}&endDate={end_date}&lat={lat_long[0]}&lng={lat_long[1]}&radius=20000'
                print(url)
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

                return list(set(links))


links = scrape_data(start_date, end_date, city, state)

list_of_accidents = []
list_of_occupants = []
list_of_vehicles = []

for i in links:
        try:
                accident_data, vehicle_data, occupant_data = get_page_data(i, list_of_vehicles, list_of_occupants)
                list_of_accidents.append(accident_data)
        except:
                continue

store_to_cloud('accidents', list_of_accidents, state, city,start_date, end_date)
store_to_cloud('vehicles', list_of_vehicles, state, city,start_date, end_date)
store_to_cloud('occupants', list_of_occupants, state, city,start_date, end_date)