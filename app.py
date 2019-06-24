from flask import Flask,jsonify,request,url_for

app = Flask(__name__)

measurements = []

# GET measurements data
@app.route('/api/v1/measurements')
def get_measurements():
    request_data = request.get_json()
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
    if measurements:
        _id =  max([ m['id'] for m in measurements]) + 1
    else:
        _id = 1

    measurement = {
        "id" : _id,
        "timestamp": request_data["timestamp"],
        "sensor": request_data["sensor"],
        "value": request_data["value"],
    }
    print("create_measurement:", request_data)
    measurements.append(measurement)
    return jsonify(measurement), 201, {"Location": url_for('get_measurement', _id=_id)}

if __name__ == "__main__":
    print(app.url_map)
    app.run(port=5000)
