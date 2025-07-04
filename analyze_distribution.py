import requests
import matplotlib.pyplot as plt
import json

def fetch_bulk_data(host, request_ids):
    """
    Send bulk requests to the load balancer and return request counts.
    :param host: Load balancer host (e.g., localhost:6000)
    :param request_ids: List of request IDs
    :return: Dictionary of request counts per server
    """
    url = f"http://{host}/bulk"
    payload = {"request_ids": request_ids}
    try:
        response = requests.post(url, json=payload, timeout=100)
        response.raise_for_status()
        data = response.json()
        return data.get("request_counts", {})
    except requests.RequestException as e:
        print(f"Error fetching bulk data: {e}")
        return {}

def plot_request_distribution(request_counts, output_file="request_distribution.png"):
    """
    Generate a bar chart of request counts per server.
    :param request_counts: Dictionary of server names to request counts
    :param output_file: Output file name for the chart
    """
    servers = list(request_counts.keys())
    counts = list(request_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, counts, color='skyblue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Request Distribution Across Servers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Chart saved as {output_file}")

if __name__ == "__main__":
    # Send 1000 requests for analysis
    request_ids = list(range(100))
    host = "localhost:6000"
    request_counts = fetch_bulk_data(host, request_ids)
    if request_counts:
        plot_request_distribution(request_counts)