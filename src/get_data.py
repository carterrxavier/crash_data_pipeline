from selenium.webdriver.common.by import By

def get_accident_data(driver): 
    #Unique Identifier for the accident
    uids = driver.find_elements(By.ID,'accident-top')
    case_id = ''
    crash_id = ''
    for uid in uids:
        ids = uid.text.split('\n')
        for id in ids:
            if 'Case ID' in id:
                case_id = id.split(':')[1]
            elif 'Crash ID' in id:
                crash_id = id.split(':')[1]

    #Location of accident
    location = driver.find_elements(By.ID,'accident-header')
    city = None
    date = None
    police_dept = None
    for loc in location:
        location_data = loc.text.split('\n')
        city = location_data[1]
        date = location_data[3]
        police_dept = location_data[5]

    #Look into google map picture to find the lat and long of the crash
    crash_lat = None
    crash_long = None
    pictures = driver.find_elements(By.TAG_NAME, 'img')
    for pic in pictures:
        if 'https://maps.googleapis.com' in pic.get_attribute('src'):
            current_src = pic.get_attribute('src')
            split = current_src.split('=')[1].replace('&style', '').split(',')
            crash_lat = split[0]
            crash_long = split[1]

    #grab accident contributing factors
    rows = driver.find_elements(By.CLASS_NAME,'row')
    summary = rows[0].text.split('\n')
    #check to see if the text in the next index is a header to the next value,
    #if it is , then the value is null, we will insert a null value into this index
    #if the text following the header is not the next header, then thats the value needed to be stored
    if summary[summary.index('Accident Contributing Factors') + 1] == 'Date & Time Of Crash':
        summary.insert(summary.index('Accident Contributing Factors') + 1, None)
    if summary[summary.index('Date & Time Of Crash') + 1] == 'Speed Limit':
        summary.insert(summary.index('Date & Time Of Crash') + 1, None)
    if summary[summary.index('Speed Limit') + 1] == any(char.isdigit() for char in summary[summary.index('Speed Limit') + 1]):
        summary.insert(summary.index('Speed Limit') + 1, None)
    if summary[summary.index('Total Number of Injuries') - 1].isdigit() == False:
        summary.insert(summary.index('Total Number of Injuries') - 1, None)
    if summary[summary.index('Total Number of Vehicles') - 1].isdigit() == False:
        summary.insert(summary.index('Total Number of Vehicles') - 1, None)
    if summary[summary.index('Total Number of Occupants') - 1].isdigit() == False:
        summary.insert(summary.index('Total Number of Occupants') - 1, None)
    if summary[-1] == 'Accident Location':
        summary.insert(summary.index('Accident Location') + 1, None)

    accident_factors = str(summary[summary.index('Accident Contributing Factors') \
                                   + 1:summary.index('Date & Time Of Crash')])\
                                    .replace('[','')\
                                    .replace(']','')
    
    accident_date_time = summary[summary.index('Date & Time Of Crash') + 1]
    accident_speed_limit = summary[summary.index('Speed Limit') + 1]
    accident_number_of_injuries = summary[summary.index('Total Number of Injuries') - 1]
    accident_number_of_vehicles = summary[summary.index('Total Number of Vehicles') - 1]
    accident_number_of_occupants = summary[summary.index('Total Number of Occupants') - 1]
    accident_location = summary[summary.index('Accident Location') + 1]

    summary_2 = rows[1].text.split('\n')

    if summary_2[summary_2.index('Description') + 1] == 'Road & Traffic Conditions':
        summary_2.insert(summary_2.index('Description') + 1, None)
    if summary_2[summary_2.index('Road & Traffic Conditions') + 1] == 'Weather':
        summary_2.insert(summary_2.index('Road & Traffic Conditions') + 1, None)
    if summary_2[-1] == 'Weather':
        summary_2.insert(summary_2.index('Weather') + 1, None)

    accident_description = summary_2[summary_2.index('Description') + 1]
    accident_traffic_conditions = summary_2[summary_2.index('Road & Traffic Conditions') + 1]
    accident_weather =  summary_2[summary_2.index('Weather') + 1]

    
    dictionary = {
            "case_id": case_id,
            "crash_id": crash_id,
            "city": city,
            "date": date,
            "police_dept": police_dept,
            "crash_lat": crash_lat,
            "crash_long": crash_long,
            "accident_factors": accident_factors,
            "accident_date_time": accident_date_time,
            "accident_speed_limit": accident_speed_limit,
            "accident_number_of_injuries": accident_number_of_injuries,
            "accident_number_of_vehicles": accident_number_of_vehicles,
            "accident_number_of_occupants": accident_number_of_occupants,
            "accident_location": accident_location,
            "accident_description": accident_description,
            "accident_traffic_conditions": accident_traffic_conditions,
            "accident_weather": accident_weather
            }
    return dictionary , crash_id

def get_vehicle_data(driver, crash_id, list_of_vehicles):
    vehicles = driver.find_elements(By.CLASS_NAME,'driver-vehicle')
    vehicle_number = 1
    veh_pic = []
    for vehicle in vehicles:
        vehicle_type = vehicle.find_elements(By.CLASS_NAME, 'vehicle-holder')
        for veh_type in vehicle_type:
                elements = veh_type.find_elements(By.CLASS_NAME, 'schema')
        for e in elements:
                veh_pic.append(e.get_attribute('src'))
    print(veh_pic)

    for vehicle in vehicles:
        if len(vehicle.find_elements(By.CLASS_NAME,'at-fault')) ==0:
            at_fault = 0
        else:
            at_fault = 1
        veh = vehicle.text.split('\n')
        if veh[0] == 'Driver Info Vehicle Info':
            veh.insert(veh.index('Driver Info Vehicle Info') - 1, None)
        if veh[veh.index('Damage Area') + 1] == 'Driver License Type':
            veh.insert(veh.index('Damage Area') + 1, None)

    
        if 'VIN' not in veh and veh[veh.index('Driver License Type') + 1] == 'Vehicle License State ID':
            veh.insert(veh.index('Driver License Type') + 1, 'VIN')
            veh.insert(veh.index('Driver License Type') + 2, 'NOVIN')
            
        elif 'VIN' not in veh and veh[veh.index('Driver License Type') + 1] != 'Vehicle License State ID':
            veh.insert(veh.index('Driver License Type') + 2, 'VIN')
            veh.insert(veh.index('Driver License Type') + 3, 'NOVIN')


        if veh[veh.index('Driver License Type') + 1] == 'Vehicle License State ID':
            veh.insert(veh.index('Driver License Type') + 1, None)
        if veh[veh.index('Vehicle License State ID') + 1] == 'VIN':
            veh.insert(veh.index('Vehicle License State ID') + 1, None)
        if veh[veh.index('Driver License Type') + 1] == 'VIN':
            veh.insert(veh.index('Driver License Type') + 1, None)
        if veh[veh.index('VIN') + 1] == 'Insured':
            veh.insert(veh.index('VIN') + 1, "NOVIN")
        if veh[veh.index('Insured') + 1] == 'Towing Company':
            veh.insert(veh.index('Insured') + 1, None)
        if veh[-1] == 'Towing Company':
            veh.insert(veh.index('Towing Company') + 1, None)
        if veh[-1] == 'Insured':
            veh.insert(veh.index('Insured') + 1, None)


        vehicle_description = veh[veh.index('Driver Info Vehicle Info') - 1]
        damage_area = veh[veh.index('Damage Area') + 1]
        driver_license_type = veh[veh.index('Driver License Type') + 1]
        vehicle_driver_license_state = veh[veh.index('Vehicle License State ID') + 1]
        vin_number = veh[veh.index('VIN') + 1]
        insured = veh[veh.index('Insured') + 1]
        towing_company = veh[-1]
        

        
                

        dictionary = {
            'crash_id': crash_id,
            'vehicle_id': f'{crash_id}{vin_number}{vehicle_number}',
            'vehicle_description': vehicle_description,
            'vehicle_number': vehicle_number,
            'damage_area': damage_area,
            'driver_license_type':driver_license_type,
            'vehicle_driver_license_state':vehicle_driver_license_state,
            'vehicle_src': veh_pic[vehicle_number - 1],
            'vin_number':vin_number,
            'insured':insured,
            'towing_comnpany':towing_company,
            'at_fault': at_fault
        }

        list_of_vehicles.append(dictionary)

        vehicle_number += 1
    return list_of_vehicles  