import base64
from flask import Flask, request, jsonify
import json
from src.aquire import check_city_support ,scrape_data

app = Flask(__name__)

#trigger daily, will take a request that will allow for a start date, an end date, and a city (only if the city is supported)
@app.route("/start_scrape", methods=["POST"])
def scrape():
    data = request.get_json()  # Extract JSON data from the request
    message_data_base64 = data.get('message', {}).get('data', '')  # Extract base64 encoded message data
    if message_data_base64:
            message_data_json = base64.b64decode(message_data_base64).decode('utf-8')  # Decode base64 and parse JSON
            message_data = json.loads(message_data_json)
            start_time = message_data.get('start_time')
            end_time = message_data.get('end_time')
            city = message_data.get('city')
            print("Received data: start_time={}, end_time={}, city={}".format(start_time, end_time, city))
            lat_long = check_city_support(city)
            if lat_long:
                  scrape_data(start_time,end_time, city)
            # Now you can use start_time, end_time, and city in your application logic
            return jsonify({"message": "Data received successfully."}), 200
    return jsonify({"error": "Invalid request."}), 400

if __name__ == '__main__':
      app.run(debug=True)