from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # allows cross-origin from your frontend

@app.route('/event', methods=['POST'])
def receive_event():
    data = request.json
    print("Received Event:", data)
    # Do something with the event (e.g., store it)
    return jsonify({"status": "success", "received": data}), 200

if __name__ == '__main__':
    conn = sqlite3.connect('example.db')

    app.run(host='0.0.0.0', port=5000)