from flask import Flask,jsonify,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import datetime as dt

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Measurement

# GET measurements data
@app.route('/api/v1/measurements')
def get_measurements():
    measurements = []
    query =  Measurement.query
    if 'sensor' in request.args:
        query = query.filter(Measurement.sensor == request.args.get('sensor'))

    if 'ts_start' in request.args:
        query = query.filter(Measurement.timestamp >= dt.datetime.strptime(request.args.get('ts_start'), "%Y-%m-%d %H:%M:%S"))

    if 'ts_end' in request.args:
        query = query.filter(Measurement.timestamp <= dt.datetime.strptime(request.args.get('ts_end'), "%Y-%m-%d %H:%M:%S"))

    for measurement in query.all():
        measurements.append(measurement.serialize())
    return jsonify({'measurements': measurements})

@app.route('/api/v1/measurements/<int:_id>', methods=['GET'])
def get_measurement(_id):
    match = db.session.query(Measurement).filter(Measurement.id == _id).first()
    if match:
        return jsonify(match.serialize())
    return "", 404

@app.route('/api/v1/measurements', methods=['POST'])
def create_measurement():
    request_data = request.get_json()
    auth = request.headers.get("X-Api-Key")

    # For creating measurements you need a valid API key
    if auth != app.config["API_KEY"]:
        return jsonify({"message": "ERROR: Unauthorized or missing API key"}), 401

    measurement = Measurement(
#        "id" : _id,
        sensor=request_data["sensor"],
        timestamp=dt.datetime.strptime(request_data["timestamp"], "%Y-%m-%d %H:%M:%S"),
        value=request_data["value"],
    )
    db.session.add(measurement)
    db.session.commit()
    return jsonify(measurement.serialize()), 201, {"Location": url_for('get_measurement', _id=measurement.id)}

if __name__ == "__main__":
    print(app.url_map)
    app.run(port=5000)
