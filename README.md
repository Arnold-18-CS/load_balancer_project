# Load Balancer Project

## Server Implementation (Task 1)

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

## Server Containerization

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