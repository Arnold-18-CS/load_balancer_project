# Load Balancer Project

## Server Implementation (Task 1.1)

### Task 1 Overview
The server is a Flask-based web server implemented in `server/app.py`. It runs on port 5000 and provides two endpoints:
- `/home` (GET): Returns a JSON response with a unique server ID (set via the `SERVER_ID` environment variable) and status.
- `/heartbeat` (GET): Returns an empty JSON response to indicate the server is alive.

### How to Run Basic Server
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Set the SERVER_ID environment variable using
    ```bash
    export SERVER_ID = 3
    ```

3. Run the server
    ```bash
    python server/app.py
    ```

4. Test the endpoints on this link `http://localhost:5000` with 2 endpoints `/home` and `/heartbeat`.

## Server Containerization (Task 1.2)

### Overview
The Flask server is containerized using a `Dockerfile` in the `server` directory. The image includes the Flask application (`app.py`) and dependencies (`requirements.txt`).

### Dockerfile Details
- Base Image: `python:3.12-slim`
- Port: 5000
- Environment Variable: `SERVER_ID` (default: `Unknown`)
- Command: `python app.py`

### How to Build and Run
1. Ensure Docker is installed and running.

2. Build the Docker image:
   ```bash
   docker build -t load-balancer-server .
   ```

3. Run the container with a custom SERVER_ID:
    ```bash
    docker run --rm -p 5000:5000 -e SERVER_ID=1 load-balancer-server
    ```

4. Test the endpoints:
    ```bash
    curl http://localhost:5000/home
    curl http://localhost:5000/heartbeat
    curl http://localhost:5000/bad # Should return a 404 status error 
    ```

## Consistent Hash Map Implementation (Task 2.1)

### Overview
The consistent hash map is implemented in `hash_map/consistent_hash.py` to map client requests to one of N=3 server replicas using a hash ring with 512 slots and 9 virtual servers per physical server.

### Implementation Details
- **Parameters**:
  - Hash slots: 512
  - Servers: 3 (Server1, Server2, Server3)
  - Virtual servers per server: 9
  - Virtual server hash: Φ(i, j) = i + j + 2j + 25
  - Request hash: H(i) = i + 2i + 2172
- **Data Structure**: A 512-slot array (`hash_ring`) stores server names, with a dictionary (`server_to_slots`) tracking each server’s slots.
- **Conflict Resolution**: Linear probing resolves slot conflicts for virtual servers.
- **Methods**:
  - `__init__`: Initializes the hash ring with 3 servers and 9 virtual servers each.
  - `_virtual_server_hash`: Computes slot for virtual servers.
  - `_request_hash`: Computes slot for requests.
  - `_populate_ring`: Places virtual servers on the ring.
  - `add_server`: Adds a new server with 9 virtual servers.
  - `remove_server`: Removes a server and its virtual servers.
  - `get_server`: Maps a request ID to the nearest server (clockwise).

### Design Choices
- Used a simple array for the hash ring to match the assignment’s suggestion.
- Linear probing was chosen for simplicity and effectiveness in resolving conflicts.
- The `server_to_slots` dictionary simplifies server removal by tracking slot assignments.
- Hash functions are implemented exactly as specified to ensure consistent distribution.

