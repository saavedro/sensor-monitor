from flask import Flask,jsonify,request,url_for

app = Flask(__name__)

# GET measurements data
@app.route('/api/v1/measurements')
def get_measurements():
    request_data = request.get_json()
    return jsonify({'measurements': []})

@app.route('/api/v1/measurements/<int:id>', methods=['GET'])
def get_measurement(id):
    return jsonify({})

@app.route('/api/v1/measurements', methods=['POST'])
def create_measurement():
    request_data = request.get_json()
    print("create_measurement:", request_data)
    return jsonify(request_data), 201, {"Location": url_for('get_measurement', id=1)}

if __name__ == "__main__":
    print(app.url_map)
    app.run(port=5000)
