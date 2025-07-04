#!/bin/bash

  # Script to set up and test the load balancer project
  # Usage: ./run_tests.sh
  # Prerequisites: Docker installed, WSL Ubuntu 20.04, VS Code with REST Client extension

  echo "Setting up load balancer project..."

  # Install matplotlib for chart generation
  echo "Installing matplotlib..."
  pip install matplotlib

  # Navigate to project directory
  cd ~/load_balancer_project

  # Build server image
  echo "Building load-balancer-server image..."
  cd server
  docker build -t load-balancer-server .
  cd ..

  # Build load balancer image
  echo "Building load-balancer image..."
  docker build -t load-balancer .

  # Create Docker network
  echo "Creating Docker network..."
  docker network rm load-balancer-net 2>/dev/null
  docker network create load-balancer-net

  # Run server containers
  echo "Starting server containers..."
  docker rm -f server1 server2 server3 server4 2>/dev/null
  docker run -d --name server1 --network load-balancer-net -e SERVER_ID=1 load-balancer-server
  docker run -d --name server2 --network load-balancer-net -e SERVER_ID=2 load-balancer-server
  docker run -d --name server3 --network load-balancer-net -e SERVER_ID=3 load-balancer-server

  # Run load balancer container
  echo "Starting load balancer container..."
  docker rm -f load-balancer 2>/dev/null
  docker run -d --name load-balancer --network load-balancer-net -p 6000:6000 load-balancer

  # Wait for containers to start
  echo "Waiting for containers to stabilize..."
  sleep 5

  # Verify containers are running
  echo "Checking running containers..."
  docker ps

  # Generate request distribution chart
  echo "Generating request distribution chart..."
  python3 analyze_distribution.py

  # Instructions for testing
  echo "Setup complete! To test endpoints:"
  echo "1. Open ~/load_balancer_project/load_balancer_tests.http in VS Code."
  echo "2. Ensure the REST Client extension (humao.rest-client) is installed."
  echo "3. Click 'Send Request' above each request in load_balancer_tests.http."
  echo "4. To test server-specific endpoints (/home, /heartbeat), set {{server_host}} to server1:5000, server2:5000, or server3:5000."
  echo "5. To test adding a server, first run:"
  echo "   docker run -d --name server4 --network load-balancer-net -e SERVER_ID=4 load-balancer-server"
  echo "6. To test 503 error, stop servers:"
  echo "   docker stop server1 server2 server3 server4"
  echo "7. Check request distribution chart: ~/load_balancer_project/request_distribution.png"
  echo "8. To clean up, run:"
  echo "   docker stop load-balancer server1 server2 server3 server4"
  echo "   docker network rm load-balancer-net"