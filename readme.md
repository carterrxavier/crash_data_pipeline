# Crash Data Pipeline

This repository stores the process to extract data from BigQuery and encrypt it into a GCS storage bucket. It has the optional capability to also encrypt said file data with PGP encryption. It is integrated with GCP BigQuery & Cloud Storage to write data to a given bucket and hosted on GCP Cloud Run as multiple routes on a Flask application.

## System Requirements

- [Python 3](https://www.python.org/downloads/)
- [gcloud CLI](https://cloud.google.com/sdk/gcloud)

## Project Structure

```bash
|—src # source code for processing
|—.gitignore # gitignore
|—Dockerfile # Dockerfile for container image definition
|—main.py # entry point for Flask service with route defintions
|—requirements.txt # deployment project dependencies
```

## Setup

To setup the project, create a virtual environment through python-venv, [virtualenv](https://pypi.org/project/virtualenv/) or a virtual environment manager of choice and install dependencies with:

```bash
> pip install -r requirements.txt
```

## Code Execution

If your looking to parse new data manually after local enviroment has  been set up you will run the code
```bash
> cd src
> python aquire.py
```

To manually run the python script to add any new data to Bigquery, make sure that the virtual environment is activated. Execute the following:

```bash
> python run main.py
```


## Code Deployment

The deployment of the code is configured using GCP Cloud Build. This file contains the steps taken when a commit is made against the `main` branch. No additional work is needed to deploy the code, but to manually deploy the code, run the following:

```bash
> gcloud builds submit --config cloudbuild.yaml
```

For this, substitutions for variables will need to be made inside of the cloudbuild.yaml file, which can be found at the top of the file.
