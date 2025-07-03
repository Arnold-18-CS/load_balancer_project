# Use official python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port the Flask server runs on
EXPOSE 5000

# Set the environment variable (SERVER_ID) for Flask
ENV SERVER_ID=Unknown

# Command to run the Flask application
CMD ["python", "app.py"]

# To run this Dockerfile, you can build the image and run it with the following commands:
# docker build -t load-balancer-server .

# Note: The SERVER_ID environment variable can be set at runtime to differentiate between multiple instances.
# Example: docker run --rm -e SERVER_ID=1 -p 5000:5000 load-balancer-server
# This will run the server with SERVER_ID set to 1.

# The server can be accessed at http://localhost:5000/ with the SERVER_ID displayed in the response.