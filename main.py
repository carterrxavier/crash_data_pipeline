from flask import Flask, request, jsonify
from google.cloud import storage
from datetime import datetime, timedelta, timezone
import os
from src.store_to_gcs import stitch_data, store_to_bigquery
from src.last_run import get_last_message_timestamp

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


project_id = os.environ.get('PROJECT_ID')
bucket_name = os.environ.get('BUCKET_NAME')
subscription_name = os.environ.get("PUB_SUB_NAME")

#trigger daily, will check to see if there were any files 
#created in the GCS bucket in the last 24 hours
#if they exist, stitch the json files together and store to BQ
@app.route("/", methods=["POST"])
def store_to_bq():
      client = storage.Client(project=project_id)
      bucket = client.get_bucket(bucket_name)

      accident_data = []
      vehicle_data = []
      occupant_data = []
      time_threshold =  (datetime.today() - timedelta(hours=24)).replace(tzinfo=timezone.utc)
      blobs = bucket.list_blobs()
      recent_files = [blob.name for blob in blobs if blob.time_created >= time_threshold]

      for file in recent_files:
            stitch_data('accidents', file, accident_data)
            stitch_data('vehicles', file, vehicle_data)
            stitch_data('occupants', file, occupant_data)

      store_to_bigquery(accident_data,'accidents')
      store_to_bigquery(vehicle_data,'vehicles')
      store_to_bigquery(occupant_data,'occupants')
      
      return "success",200
store_to_bq()