import requests
from requests.exceptions import RequestException
import matplotlib.pyplot as plt
import time
import os

def reset_request_counts(host):
    """
    Reset request counts on the load balancer by restarting it.
    :param host: Load balancer host (e.g., localhost:6000)
    """
    try:
        # Stop and restart load balancer to reset counts
        os.system("docker restart load-balancer")
        time.sleep(5)  # Wait for restart
        print("Request counts reset by restarting load balancer")
    except Exception as e:
        print(f"Error resetting request counts: {e}")

def fetch_bulk_data(host, request_ids, max_retries=3, timeout=500):
    """
    Send bulk requests to the load balancer and return request counts.
    :param host: Load balancer host (e.g., localhost:6000)
    :param request_ids: List of request IDs
    :param max_retries: Number of retries for failed requests
    :param timeout: Request timeout in seconds
    :return: Dictionary of request counts per server
    """
    url = f"http://{host}/bulk"
    payload = {"request_ids": request_ids}
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("request_counts", {})
        except RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    print(f"Error: Failed to fetch bulk data after {max_retries} attempts")
    return {}

def plot_request_distribution(request_counts, output_file="request_distribution.png"):
    """
    Generate a bar chart of request counts per server.
    :param request_counts: Dictionary of server names to request counts
    :param output_file: Output file name for the chart
    """
    if not request_counts:
        print("No request counts to plot")
        return
    servers = list(request_counts.keys())
    counts = list(request_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, counts, color='skyblue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Servers')
    plt.xticks(rotation=45)
    for i, count in enumerate(counts):
        plt.text(i, count + 0.5, str(count), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Chart saved as {output_file}")

if __name__ == "__main__":
    host = "localhost:6000"
    # Reset request counts
    reset_request_counts(host)
    # Send 1000 requests for analysis
    request_ids = list(range(1000))
    request_counts = fetch_bulk_data(host, request_ids)
    if request_counts:
        plot_request_distribution(request_counts)
    else:
        print("Failed to generate chart due to connection issues")