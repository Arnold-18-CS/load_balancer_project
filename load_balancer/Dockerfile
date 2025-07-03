# Use official Python 3.8 slim image as base (compatible with Ubuntu 20.04)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy load balancer and hash map code
COPY app.py .
COPY ../hash_map/consistent_hash.py .

# Expose port 6000 for the load balancer
EXPOSE 6000

# Run the Flask application
CMD ["python", "app.py"]