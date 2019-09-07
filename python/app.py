from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_caching import Cache
from datetime import date
import requests

AVAILABILITY_URL = "https://www.thinkful.com/api/advisors/availability"

app = Flask(__name__)
CORS(app)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
CACHE_KEY="BOOKED"

def get_dict_for_cache_string(cache_string):
    split_string = cache_string.split(";")
    return {
        'provider_id': split_string[0],
        'timestamp': split_string[1],
        'name': split_string[2]
    }

def get_booked_dictionary():
    booked_array = cache.get(CACHE_KEY)
    if booked_array is None:
        booked_array = []
    return map(lambda x: get_dict_for_cache_string(x),booked_array)

def book_appointment(provider_id, timeslot, name):
    booked_string=format_cached_string(provider_id, timeslot, name)
    booked_array = cache.get(CACHE_KEY)
    if booked_array is None:
        booked_array = []
    booked_array.append(booked_string)
    cache.set(CACHE_KEY, booked_array)

def time_is_in_cache(cache_string_no_name):
    booked_array = cache.get(CACHE_KEY)
    if booked_array is None:
        booked_array = []
    if any(cache_string_no_name in s for s in booked_array):
        return True
    return False

def format_cached_string(provider_id, timeslot, name):
    # Store booked times as a formatted string, to ease simplicity
    return "%s;%s;%s"%(provider_id,timeslot, name)

def check_for_booked_time(provider_id, timeslot):
    booked_string=format_cached_string(provider_id, timeslot,'')
    return time_is_in_cache(booked_string)

def fetch_availability_data():
    r = requests.get(url=AVAILABILITY_URL)
    data = r.json()
    return data

def transform_availability_list(data_from_endpoint):
    provider_dict = dict()
    for day, entries in data_from_endpoint.items():
        for time, id in entries.items():
            if not check_for_booked_time(id, time):
                availability = provider_dict.get(id, [])
                availability.append(time)
                provider_dict[id] = availability
    return provider_dict

@app.route("/today", methods=["GET"])
def today():
    return jsonify({"today": date.today().isoformat()})

@app.route("/times_by_advisor_id", methods=["GET"])
def times_by_advisor_id():
    data_from_endpoint = fetch_availability_data()
    provider_dict = transform_availability_list(data_from_endpoint)
    return jsonify(provider_dict)

@app.route("/booked_times", methods=["GET"])
def booked_times():
    return jsonify(get_booked_dictionary())

@app.route("/book", methods=["POST"])
def book():
    req_data = request.get_json()
    provider_id = req_data['provider_id']
    timestamp = req_data['timestamp']
    name = req_data['name']
    if check_for_booked_time(provider_id,timestamp):
        abort(403)
    else:
        book_appointment(provider_id, timestamp, name)
        return "OK", 200