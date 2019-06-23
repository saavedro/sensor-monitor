import pytest
from app import app

@pytest.fixture(scope='module')
def test_app():
    app.testing = True
    yield app.test_client()

def test_measurements_get(test_app):
    rv = test_app.get('/api/v1/measurements')
    assert rv.status_code == 200
