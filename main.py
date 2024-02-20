from flask import Flask, request
import json
from src.aquire import scrape_data

app = Flask(__name__)

#trigger daily, will take a request that will allow for a start date, an end date, and a city (only if the city is supported)
@app.route("/start_scrape", methods=["POST"])
def scrape():
    data = json(request.data.decode('utf-8'))
    print("I SEE YOU")
    print(data)
    return 'success',200
