import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os


options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
pattern = r"https://app\.myaccident\.org/accident/\d+$"


def check_city_support(city):
        city_coordinates = {
                'houston': [29.7604, -95.3698],
                'san antonio': [29.4241, -98.4936],
                'dallas': [32.7767, -96.7970],
                'austin': [30.2672, -97.7431],
                'fort worth': [32.7555, -97.3308],
                'el paso': [31.7619, -106.4850],
                'arlington': [32.7357, -97.1081],
                'corpus christi': [27.8006, -97.3964],
                'plano': [33.0198, -96.6989],
                'laredo': [27.5306, -99.4803],
                'lubbock': [33.5779, -101.8552],
                'garland': [32.9126, -96.6389],
                'irving': [32.8140, -96.9489],
                'amarillo': [35.2210, -101.8313],
                'grand prairie': [32.7459, -96.9978],
                'brownsville': [25.9018, -97.4975],
                'mckinney': [33.1972, -96.6397],
                'frisco': [33.1507, -96.8236],
                'pasadena': [29.6911, -95.2091],
                'mesquite': [32.7668, -96.5992],
                'killeen': [31.1171, -97.7278],
                'mcallen': [26.2034, -98.2300],
                'carrollton': [32.9756, -96.8897],
                'beaumont': [30.0802, -94.1266],
                'round rock': [30.5083, -97.6789],
                'waco': [31.5493, -97.1467],
                'denton': [33.2148, -97.1331],
                'midland': [31.9973, -102.0779],
                'wichita falls': [33.9137, -98.4934]
        }
        return city_coordinates.get(city.lower())
        
def scrape_data(start_date, end_date, city):  

        url = 'https://app.myaccident.org/results?startDate=2024-02-01&endDate=2024-02-18&lat=32.7767&lng=-96.7970&radius=20000'

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
