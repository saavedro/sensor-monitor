import pytest
from app import app

@pytest.fixture(scope='module')
def test_app():
    app.testing = True
    yield app.test_client()

def test_get_measurements(test_app):
    rv = test_app.get('/api/v1/measurements')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/json'

def test_create_measurement(test_app):
    data = {
        "sensor": "test",
        "value": "10.00",
        "timestamp": "2019-06-23 12:38"}
    rv = test_app.post('/api/v1/measurements', json=data)
    assert rv.status_code == 201
    assert "/api/v1/measurements/" in rv.headers['Location']
