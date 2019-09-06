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
