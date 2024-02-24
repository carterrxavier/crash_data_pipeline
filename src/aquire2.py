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
from get_data import get_accident_data, get_vehicle_data


def get_page_data(link, list_of_vehicles, list_of_occupants):
    
    options = webdriver.ChromeOptions()
    dir_path = os.path.dirname(os.path.realpath('chromedriver'))
    chromedriver = dir_path + '/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    print(f"Parsing data from {link}")
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    try:
        ui.WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'container')))
        #get accident summary data
        accident_data, crash_id = get_accident_data(driver)
        list_of_vehicles, vehicle_id = get_vehicle_data(driver, crash_id, list_of_vehicles)
        get_occupant_data(driver, vehicle_id, list_of_occupants)
                
    except TimeoutException as ex:
        print("Bad Link, skipping Link")
        driver.close()
    
    return accident_data, list_of_vehicles
    



