import os
from google.cloud import storage
from google.cloud import bigquery
import json
from dotenv import load_dotenv
load_dotenv()


project_id = os.environ.get('PROJECT_ID')
bucket_name = os.environ.get('BUCKET_NAME')
dataset_id = os.environ.get("DATASET_ID")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

client = storage.Client(project=project_id)
bucket = client.get_bucket(bucket_name)

def store_to_cloud(file_type,file, state, city, start_date, end_date):
    filename = f'{state}/{city}/{file_type}/{start_date}__{end_date}.json'

    json_string = json.dumps(file)

    blob = bucket.blob(filename)

    blob.upload_from_string(json_string)

    print(f"JSON data has been uploaded to {blob.public_url}")

def stitch_data(file_type, file_name, file_stitch):  
    if file_type in file_name:
        print(file_name)
        blob = bucket.blob(file_name)
        json_string = blob.download_as_string()
        json_data = json.loads(json_string)
        file_stitch += json_data

def store_to_bigquery(json_data,table):

    # Replace these variables with your actual values
    table_id = table

    # Initialize a client
    client = bigquery.Client(project=project_id)

    # Check if the dataset exists, and create it if it doesn't
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    try:
        client.get_dataset(dataset_ref)
    except:
        dataset = client.create_dataset(dataset)
        client.get_dataset(dataset_ref)


    # Infer schema from the JSON data
    first_json_object = json_data[0]
    print(first_json_object)

    schema = []
    for key in first_json_object.keys():
        # Add each key-value pair as a field in the schema
        schema.append(bigquery.SchemaField(key, "STRING"))
    

    # Create or get the table reference
    try:
        table_ref = dataset_ref.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        client.get_table(table_ref)
    except:
        # Create the table with the inferred schema
        table = client.create_table(table)
        table_ref = dataset_ref.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        client.get_table(table_ref)
        
    # Load the JSON data into BigQuery
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job = client.load_table_from_json(json_data, table_ref, job_config=job_config)

    # Wait for the job to complete
    job.result()

    print(f"Loaded {job.output_rows} row(s) into {table_id}")
