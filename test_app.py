import pytest

import os
os.environ['APP_SETTINGS'] = "config.TestingConfig"

from app import app, db, Measurement
import flask_migrate

@pytest.fixture()
def test_client():

    # Setting the database
    db.create_all()

    yield app.test_client()

    db.drop_all()

def test_get_measurements(test_client):
    rv = test_client.get('/api/v1/measurements')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/json'

def test_create_measurement(test_client):
    data = {
        "sensor": "test",
        "value": "10.00",
        "timestamp": "2019-06-23 12:38:01"}
    rv = test_client.post('/api/v1/measurements', json=data)
    assert rv.status_code == 201
    assert "/api/v1/measurements/" in rv.headers['Location']

def test_get_single_measurement(test_client):
    data = {
        "id": 2,
        "sensor": "test",
        "value": "12.34",
        "timestamp": "2019-06-23 12:38:01"}

    m = Measurement(**data)
    db.session.add(m)

    rv = test_client.get('/api/v1/measurements' + '/' + str(data['id']))
    assert rv.status_code == 200
    assert rv.json == data
@pytest.fixture
def sample_search_data():
    search_data = [
        {"id": 2, "sensor": "s1", "value": "12.34", "timestamp": "2019-06-23 12:38:01"},
        {"id": 3, "sensor": "s2", "value": "12.35", "timestamp": "2019-06-23 12:38:02"},
        {"id": 4, "sensor": "s1", "value": "12.36", "timestamp": "2019-06-23 12:38:03"},
    ]
    for d in search_data:
        m = Measurement(**d)
        db.session.add(m)

def test_search_by_sensor_name(test_client, sample_search_data):
    params = {'sensor':'s1'}
    rv = test_client.get('/api/v1/measurements', query_string=params)
    assert rv.status_code == 200
    measurements = rv.json['measurements']
    assert len(measurements) == 2 # s2 does not match
    assert set(m['id'] for m in measurements) == set([2, 4])

def test_search_by_sensor_ts_start(test_client, sample_search_data):
    params = {'ts_start':'2019-06-23 12:38:02'}
    rv = test_client.get('/api/v1/measurements', query_string=params)
    assert rv.status_code == 200
    measurements = rv.json['measurements']
    assert len(measurements) == 2
    assert set(m['id'] for m in measurements) == set([3, 4])

def test_search_by_sensor_ts_end(test_client, sample_search_data):
    params = {'ts_end':'2019-06-23 12:38:02'}
    rv = test_client.get('/api/v1/measurements', query_string=params)
    assert rv.status_code == 200
    measurements = rv.json['measurements']
    assert len(measurements) == 2
    assert set(m['id'] for m in measurements) == set([2, 3])

def test_search_by_sensor_time_and_name(test_client, sample_search_data):
    params = {'sensor': 's1', 'ts_start':'2019-06-23 12:38:02'}
    rv = test_client.get('/api/v1/measurements', query_string=params)
    assert rv.status_code == 200
    measurements = rv.json['measurements']
    assert len(measurements) == 1
    assert set(m['id'] for m in measurements) == set([4])
