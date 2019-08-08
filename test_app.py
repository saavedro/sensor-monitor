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
    
