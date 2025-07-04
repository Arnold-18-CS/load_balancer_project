from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get server ID from environment variable
SERVER_ID = os.getenv('SERVER_ID', 'Unknown')

@app.route('/home', methods=['GET'])
def home():
    """
    Return a greeting message with the server ID.
    :return: JSON response with server ID and status.
    """
    return jsonify({
        "message": f"Hello from Server: {SERVER_ID}",
        "status": "successful"
    }), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    """
    Return a simple response to indicate the server is alive.
    :return: JSON response with server ID and alive status.
    """
    return jsonify({
        "server_id": SERVER_ID,
        "status": "alive"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)