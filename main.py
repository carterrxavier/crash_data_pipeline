from flask import Flask, request, jsonify
from google.cloud import storage
from datetime import datetime, timedelta, timezone
import os
from src.store_to_gcs import stitch_data, store_to_bigquery, get_unique_city_states
from src.last_run import get_last_message_timestamp

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

project_id = os.environ.get('PROJECT_ID')
bucket_name = os.environ.get('BUCKET_NAME')
subscription_name = os.environ.get("PUB_SUB_NAME")
'''
trigger daily, will check to see if there were any json files 
created in the GCS bucket in the last 24 hours
if they exist, stitch the json files together and store to BQ
'''

#entry point for pub sub push subscription
@app.route("/", methods=["POST"])
def store_to_bq():
      client = storage.Client(project=project_id)
      bucket = client.get_bucket(bucket_name)

      
      time_threshold =  (datetime.today() - timedelta(hours=24)).replace(tzinfo=timezone.utc)
      blobs = bucket.list_blobs()

      #limit files to only those created in last 24 hours
      recent_files = [blob.name for blob in blobs if blob.time_created >= time_threshold]
      city_state = []

      #first get all unique city state combos from file name
      for file in recent_files:
            state = file.split('/')[0]
            city = file.split('/')[1]
            city_state.append([city,state])

      unique_city_state = get_unique_city_states(city_state)


      #upload to Bigquery
      for city_state in unique_city_state:
            blobs = bucket.list_blobs()
            current_files = [blob.name for blob in blobs if city_state[0] in blob.name and city_state[1] in blob.name and blob.time_created >= time_threshold]
            file_stitch_accidents = []
            file_stitch_occupants = []
            file_stitch_vehicles = []
            for file in current_files:
                  stitch_data('accidents', file, file_stitch_accidents)
                  stitch_data('occupants', file, file_stitch_occupants)
                  stitch_data('vehicles', file, file_stitch_vehicles)
            store_to_bigquery(file_stitch_accidents,f"{city_state[0].replace(' ','_')}_{city_state[1].replace(' ','_')}_accidents")
            store_to_bigquery(file_stitch_occupants,f"{city_state[0].replace(' ','_')}_{city_state[1].replace(' ','_')}_occupants")
            store_to_bigquery(file_stitch_vehicles,f"{city_state[0].replace(' ','_')}_{city_state[1].replace(' ','_')}_vehicles")

      return "success",200
store_to_bq()
