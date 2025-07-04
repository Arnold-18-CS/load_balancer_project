# Load Balancer Project Process

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

## Consistent Hash Map Testing (Task 2.2)

### Overview
The consistent hash map (`hash_map/consistent_hash.py`) was tested using Python’s `unittest` framework in `tests/test_consistent_hash.py` to verify correct initialization, virtual server placement, request mapping, and server addition/removal.

### Testing Steps
1. Ensure the virtual environment is active:
   ```bash
   cd ~/load_balancer_project
   source venv/bin/activate
   ```

2. Run unit tests that were setup
  ```bash
  python -m unittest tests/test_consistent_hash.py -v
  ```

3. Tests performed:
  - Initialization: Verifies 512 slots, 3 servers, 9 virtual servers each, and 27 total virtual servers.
  - Virtual Server Placement: Checks Φ(i, j) = i + j + 2j + 25 with linear probing.
  - Request Mapping: Tests H(i) = i + 2i + 2172 for sample requests.
  - Add Server: Adds Server4 and verifies 9 new slots.
  - Remove Server: Removes Server1 and verifies slots are cleared.

## Load Balancer Implementation (Task 3.1)

### Overview
The load balancer is implemented in `load_balancer/app.py` using Flask. It uses the `ConsistentHashMap` from Task 2 to distribute requests across 3 server replicas and supports adding/removing servers dynamically.

### Implementation Details
- **Endpoints**:
  - `GET /<int:request_id>`: Forwards requests to a server based on the consistent hash map. Returns server’s `/home` response or 503 if no servers are available.
  - `POST /add`: Adds a server with JSON payload `{"server_id": int, "port": int}`. Returns `{"message": "Successfully added", "status": "successful"}` (HTTP 200).
  - `POST /rm`: Removes a server with JSON payload `{"server_id": int}`. Returns `{"message": "Successfully removed", "status": "successful"}` (HTTP 200) or 404 if server not found.
- **Configuration**:
  - Runs on port 6000.
  - Uses `ConsistentHashMap` with N=3, H_slots=512, K=9.
  - Servers are addressed as `http://server<server_id>:5000` (to be updated for Docker networking).
- **Dependencies**: Flask and requests (listed in `load_balancer/requirements.txt`).
- **Dockerfile**: Located in project root, copies `hash_map/` and `load_balancer/` files.

### Design Choices
- Flask was chosen for consistency with the server implementation.
- The `requests` library simplifies HTTP forwarding to servers.
- The `servers` dictionary maps server names to addresses, updated dynamically via `/add` and `/rm`.
- Error handling ensures 503 for unavailable servers and 404 for invalid endpoints or server removal.

# Load Balance How to Use

### Overview
The server is implemented in `server/app.py`, responding to `/home` with a greeting based on `SERVER_ID`.

### Implementation Details
- **Endpoint**: `GET /home` returns `{"message": "Hello from Server: X", "status": "successful"}`.
- **Dependencies**: Flask (`server/requirements.txt`).
- **Dockerfile**: Located in `server/`, builds `load-balancer-server` image.

## Load Balancer Testing (Task 3)

### Overview
Tested with three server containers (`load-balancer-server`) in a Docker network (`load-balancer-net`).

### Setup - Automatic
1. Use the automatic script to build the complete project
  ```bash
  d ~/load_balancer_project
  chmod +x run_tests.sh
  ./run_tests.sh
  ```

### Setup - Manual
1. Build the server and load balancer images:
   ```bash
   cd ~/load_balancer_project/server
   docker build -t load-balancer-server .
   cd ~/load_balancer_project
   docker build -t load-balancer .
   ```

2. Create a Docker network:
  ```bash
  docker network create load-balancer-net
  ```

3. Run three server containers:
  ```bash
  docker run -d --name server1 --network load-balancer-net -e SERVER_ID=1 load-balancer-server
  docker run -d --name server2 --network load-balancer-net -e SERVER_ID=2 load-balancer-server
  docker run -d --name server3 --network load-balancer-net -e SERVER_ID=3 load-balancer-server
  ```

4. Run the load balancer:
  ```bash
  docker run -d --name load-balancer --network load-balancer-net -p 6000:6000 load-balancer
  ```

### Testing the services

1. Test endpoints using the `load_balancer_tests.http` file.
  - Install the REST Client extension in VS Code.
  - Open `load_balancer_tests.http` in VS Code.

### Cleaning up the setup (if manual setup was done)
1. Clean up:
  ```bash
  docker stop load-balancer server1 server2 server3 server4
  docker rm load-balancer server1 server2 server3 server4
  docker network rm load-balancer-net
  ```

### Observations
- Requests are distributed based on the consistent hash map.
- Adding/removing servers works correctly.
- Error handling meets requirements (404, 400, 503).
