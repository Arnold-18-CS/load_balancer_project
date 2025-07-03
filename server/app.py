from flask import Flask
import os

# Initialize Flask application
app = Flask(__name__)

# Get server ID from env var, defaulting it to 'Unkown' if it is not set
SERVER_ID = os.getenv('SERVER_ID', 'Unknown')
# Set it in the terminal using export SERVER_ID = Something

@app.route('/home', methods=['GET'])
def home():
    """
      Endpoint: /home (GET)
      Returns a JSON response with a unique server ID and status.
      Response format: {"message": "Hello from Server: [ID]", "status": "successful"}
      HTTP Status: 200
    """
    return {
        "message" : f"Hello from Server: {SERVER_ID}",
        "status": "Successful"
    }, 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    """
      Endpoint: /heartbeat (GET)
      Returns an empty JSON response to indicate the server is alive.
      Response format: {}
      HTTP Status: 200
    """
    return {}, 200


if __name__ == '__main__':
    # Run the server on all interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)

