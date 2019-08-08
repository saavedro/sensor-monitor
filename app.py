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
    for measurement in Measurement.query.all():
        measurements.append(measurement.serialize())
    return jsonify({'measurements': measurements})

@app.route('/api/v1/measurements/<int:_id>', methods=['GET'])
def get_measurement(_id):
    match = ( [m for m in measurements if m["id"] == _id])
    if match:
        return jsonify(match[0])
    return "", 404

@app.route('/api/v1/measurements', methods=['POST'])
def create_measurement():
    request_data = request.get_json()

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
