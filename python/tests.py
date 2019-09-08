from datetime import date
from flask import jsonify
from app import app
from app import transform_availability_list
from app import (AVAILABILITY_URL)
import requests_mock

stub_response = {
  "2019-08-27": {
    "2019-08-27T11:00:00-04:00": '372955',
    "2019-08-27T12:00:00-04:00": '372955',
    "2019-08-27T10:00:00-04:00": '372955',
    "2019-08-27T14:00:00-04:00": '372955',
    "2019-08-27T13:00:00-04:00": '372955',
    "2019-08-27T16:00:00-04:00": '372955'
  },
  "2019-08-24": {
    "2019-08-24T13:00:00-04:00": '397688',
    "2019-08-24T00:00:00-04:00": '424185',
    "2019-08-24T10:30:00-04:00": '319369',
    "2019-08-24T14:00:00-04:00": '397688',
    "2019-08-24T17:00:00-04:00": '397688',
    "2019-08-24T20:00:00-04:00": '319369',
    "2019-08-24T10:00:00-04:00": '397688',
    "2019-08-24T12:00:00-04:00": '397688',
    "2019-08-24T15:00:00-04:00": '397688',
    "2019-08-24T11:00:00-04:00": '319369',
    "2019-08-24T18:00:00-04:00": '397688',
    "2019-08-24T16:00:00-04:00": '397688'
  },
  "2019-08-25": {
    "2019-08-25T20:00:00-04:00": '319369',
    "2019-08-25T10:30:00-04:00": '319369',
    "2019-08-25T11:00:00-04:00": '319369'
  },
  "2019-08-21": {
    "2019-08-21T15:00:00-04:00": '399959',
    "2019-08-21T14:15:00-04:00": '399958',
    "2019-08-21T13:45:00-04:00": '419054',
    "2019-08-21T20:00:00-04:00": '399956',
    "2019-08-21T16:00:00-04:00": '399958',
    "2019-08-21T21:00:00-04:00": '399956',
    "2019-08-21T17:00:00-04:00": '419054',
    "2019-08-21T14:00:00-04:00": '419054',
    "2019-08-21T15:30:00-04:00": '399958',
    "2019-08-21T22:00:00-04:00": '399956',
    "2019-08-21T17:30:00-04:00": '417239',
    "2019-08-21T19:00:00-04:00": '419054',
    "2019-08-21T19:30:00-04:00": '541249',
    "2019-08-21T18:00:00-04:00": '419054',
    "2019-08-21T23:00:00-04:00": '399956',
    "2019-08-21T14:30:00-04:00": '499459',
    "2019-08-21T17:15:00-04:00": '399958',
    "2019-08-21T16:30:00-04:00": '419054'
  }
}

def test_today():
    with app.test_client() as cli:
        with requests_mock.Mocker() as m:
            m.get(AVAILABILITY_URL, json=stub_response)
            resp = cli.get('/today')
            assert resp.status_code == 200
            assert resp.json == {"today": "{}".format(date.today())}

def test_times_by_advisor_id_returns_times_ordered_by_advisor_id():
    with app.test_client() as cli:
        with requests_mock.Mocker() as m:
            m.get(AVAILABILITY_URL, json=stub_response)
            resp = cli.get('/times_by_advisor_id')
            assert '419054' in resp.json.keys()
            assert "2019-08-21T16:30:00-04:00" in resp.json['419054']

def test_today_with_no_existing_bookings_returns_correct_data():
    formatted_data = transform_availability_list(stub_response)
    with app.test_client() as cli:
        with requests_mock.Mocker() as m:
            m.get(AVAILABILITY_URL, json=stub_response)
            resp = cli.get('/times_by_advisor_id')
            assert resp.json == formatted_data

def test_booking_a_time_with_a_name_succeeds_if_available():
    with app.test_client() as cli:
        with requests_mock.Mocker() as m:
            m.get(AVAILABILITY_URL, json=stub_response)
            entry = stub_response["2019-08-27"]
            timestamp = list(entry.keys())[0]
            provider_id = entry[timestamp] 
            resp = cli.post('/book', json={
                'provider_id': provider_id,
                'name': "test",
                'timestamp': timestamp
            })
            assert resp.status_code == 200

def test_booking_a_time_with_a_name_fails_if_unavailable():
    with app.test_client() as cli:
        with requests_mock.Mocker() as m:
            m.get(AVAILABILITY_URL, json=stub_response)
            entry = stub_response["2019-08-24"]
            timestamp = list(entry.keys())[0]
            provider_id = entry[timestamp] 
            resp = cli.post('/book', json={
                'provider_id': provider_id,
                'name': "test",
                'timestamp': timestamp
            })
            assert resp.status_code == 200 
            resp = cli.post('/book', json={
                'provider_id': provider_id,
                'name': "test",
                'timestamp': timestamp
            })
            assert resp.status_code != 200 
            assert resp.data == b"Time already booked"

def test_booking_a_time_without_a_name_fails():
    with app.test_client() as cli:
        with requests_mock.Mocker() as m:
            m.get(AVAILABILITY_URL, json=stub_response)
            entry = stub_response["2019-08-24"]
            timestamp = list(entry.keys())[0]
            provider_id = entry[timestamp] 
            resp = cli.post('/book', json={
                'provider_id': provider_id,
                'timestamp': timestamp
            })
            assert resp.status_code != 200
            assert resp.data == b"Please provide a name"