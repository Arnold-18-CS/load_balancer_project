from flask import Flask, request, jsonify
import requests
from hash_map.consistent_hash import ConsistentHashMap

app = Flask(__name__)

# Initialize consistent hash map with 3 servers, 512 slots, 9 virtual servers
ch = ConsistentHashMap(num_slots=512, num_servers=3, virtual_servers=9)

# Dictionary to store server addresses
servers = {
    "Server1": "http://server1:5000",
    "Server2": "http://server2:5000",
    "Server3": "http://server3:5000"
}

@app.route('/<int:request_id>', methods=['GET'])
def forward_request(request_id):
    """
    Forward request to a server based on consistent hash map.
    :param request_id: Integer ID from the URL.
    :return: Server's response or 503 if no servers are available.
    """
    if not servers:
        return jsonify({"message": "No servers available", "status": "error"}), 503
    server_name = ch.get_server(request_id)
    if server_name not in servers:
        return jsonify({"message": "No servers available", "status": "error"}), 503
    try:
        response = requests.get(f"{servers[server_name]}/home")
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.RequestException:
        return jsonify({"message": "Server error", "status": "error"}), 503

@app.route('/add', methods=['POST'])
def add_server():
    """
    Add a new server to the hash map and server list.
    Expects JSON: {"server_id": int, "port": int}
    :return: Success message or 400 if invalid input.
    """
    data = request.get_json()
    if not data or 'server_id' not in data or 'port' not in data:
        return jsonify({"message": "Invalid request data", "status": "error"}), 400
    server_id = data['server_id']
    port = data['port']
    server_name = f"Server{server_id}"
    ch.add_server(server_name, server_id)
    servers[server_name] = f"http://server{server_id}:{port}"
    return jsonify({"message": "Successfully added", "status": "successful"}), 200

@app.route('/rm', methods=['POST'])
def remove_server():
    """
    Remove a server from the hash map and server list.
    Expects JSON: {"server_id": int}
    :return: Success message or 404 if server not found.
    """
    data = request.get_json()
    if not data or 'server_id' not in data:
        return jsonify({"message": "Invalid request data", "status": "error"}), 400
    server_id = data['server_id']
    server_name = f"Server{server_id}"
    if server_name not in servers:
        return jsonify({"message": "Server not found", "status": "error"}), 404
    ch.remove_server(server_name)
    del servers[server_name]
    return jsonify({"message": "Successfully removed", "status": "successful"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
