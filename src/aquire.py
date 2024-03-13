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


'''
This is the starting code needed to locally scrape the crash data.
At the moment, the scraper only works if the chrome driver headless 
setting is disabled and therefore not allow me to run the scraper utilizing cloud run

Once you set the city, state, start, and end date run 'python aquire.py' in the terminal.
this code will scrape all the links found related to traffic accidents in the time field specified
once completed, the window will close and  the links will be used in the next step to parse them utilizing the aquire2.py file.

'''



#specify the city, state end, and start time before running aquire.py
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
        #check to see if this city has a supported lat/long
        lat_long = check_city_support(city,state)

        if lat_long != None:
                #use lat/long for link
                url = f'https://app.myaccident.org/results?startDate={start_date}&endDate={end_date}&lat={lat_long[0]}&lng={lat_long[1]}&radius=20000'
                print(url)
                driver = webdriver.Chrome(options=options)     
                driver.get(url)

                #wait for class result to load
                links = []
                #wait until element can be seen. grab all links that match the regex 
                ui.WebDriverWait(driver, timeout=100).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result')))
                #grab href tags to grab all the links needed to scrape for the next phase
                containers = driver.find_elements(By.TAG_NAME,'a')

                #grab all links that match the regex syntax, some links are not ones that link to an accident url, we will not capture those
                for con in containers:
                        if re.match(pattern,str(con.get_attribute('href'))):
                                links.append(con.get_attribute('href'))
                driver.close()

                return list(set(links))


links = scrape_data(start_date, end_date, city, state)

list_of_accidents = []
list_of_occupants = []
list_of_vehicles = []

#once links have been aquired, utilize the for-loop to parse through each link, retreiving the data from the page and storing it in the nessarry list 
for i in links:
        try:
                accident_data, vehicle_data, occupant_data = get_page_data(i, list_of_vehicles, list_of_occupants)
                list_of_accidents.append(accident_data)
        except:
                continue
#store each list into cloud storage
store_to_cloud('accidents', list_of_accidents, state, city,start_date, end_date)
store_to_cloud('vehicles', list_of_vehicles, state, city,start_date, end_date)
store_to_cloud('occupants', list_of_occupants, state, city,start_date, end_date)
