
# Use official Python 3.8 slim image as base
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY load_balancer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy load balancer and hash map code
COPY load_balancer/app.py .
COPY hash_map/ hash_map/

# Expose port 6000 for the load balancer
EXPOSE 6000

# Run the Flask application
CMD ["python", "app.py"]