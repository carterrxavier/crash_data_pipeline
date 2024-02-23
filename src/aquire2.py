import requests, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
import time
import datetime
from get_data import get_accident_summary



def get_page_data(link):
    
    options = webdriver.ChromeOptions()
    dir_path = os.path.dirname(os.path.realpath('chromedriver'))
    chromedriver = dir_path + '/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')

    print(f"Parsing data from {link}")
    driver = webdriver.Chrome()
    driver.get(link)

    try:
        ui.WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'container')))
        #get accident summary data
        case_id,\
            crash_id,\
            city,\
            date,\
            police_dept,\
            crash_lat,\
            crash_long,\
            accident_factors,\
            accident_date_time,\
            accident_speed_limit,\
            accident_number_of_injuries,\
            accident_number_of_vehicles,\
            accident_number_of_occupants,\
            accident_location,\
            accident_description,\
            accident_traffic_condititions,\
            accident_weather = get_accident_summary(driver)
        #print(case_id, crash_id ,city, date, police_dept, crash_lat, crash_long)
            
    except TimeoutException as ex:
        print("Bad Link, skipping Link")
        driver.close()
    
    return None
    



