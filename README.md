# Load Balancer Project

## Server Implementation (Task 1)

### Task 1 Overview
The server is a Flask-based web server implemented in `server/app.py`. It runs on port 5000 and provides two endpoints:
- `/home` (GET): Returns a JSON response with a unique server ID (set via the `SERVER_ID` environment variable) and status.
- `/heartbeat` (GET): Returns an empty JSON response to indicate the server is alive.

### How to Run
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
