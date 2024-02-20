from flask import Flask, request, jsonify
import json
from src.aquire import scrape_data

app = Flask(__name__)

#trigger daily, will take a request that will allow for a start date, an end date, and a city (only if the city is supported)
@app.route("/start_scrape", methods=["POST"])
def scrape():
    data = request.get_json()  # Extract JSON data from the request
    if data:
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        city = data.get('city')
        print("Received data: ", data)
        # Now you can use start_time, end_time, and city in your application logic
        return jsonify({"message": "Data received successfully."}), 200
    else:
        return jsonify({"error": "No JSON data received."}), 400
