from flask import Flask,jsonify,request

app = Flask(__name__)

# GET measurements data
@app.route('/api/v1/measurements')
def get_measurements():
    return jsonify({'measurements': []})

if __name__ == "__main__":
    app.run(port=5000)
