from flask import Flask, jsonify
from flask_cors import CORS
from datetime import date
import requests

AVAILABILITY_URL = "https://www.thinkful.com/api/advisors/availability"


app = Flask(__name__)
CORS(app)


def fetch_availability_data():
    r = requests.get(url=AVAILABILITY_URL)
    data = r.json()
    return data

@app.route("/today", methods=["GET"])
def today():
    return jsonify({"today": date.today().isoformat()})

@app.route("/times_by_advisor_id", methods=["GET"])
def times_by_advisor_id():
    data_from_endpoint = fetch_availability_data()
    provider_dict = dict()
    for day, entries in data_from_endpoint.items():
        for time, id in entries.items():
            availability = provider_dict.get(id, [])
            availability.append(time)
            provider_dict[id] = availability
    return jsonify(provider_dict)

@app.route("/booked_times", methods=["GET"])
def booked_times():
    return jsonify({})