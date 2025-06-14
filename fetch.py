import requests

# List of URLs to fetch
urls = [
    "https://stacx.mortgageconnectlp.com/ImportProject/UpdateChecklistOnOrder/136",
    "https://stacx.mortgageconnectlp.com/ImportProject/UpdateChecklistOnOrder/137",
    "https://stacx.mortgageconnectlp.com/ImportProject/UpdateChecklistOnOrder/138",
    "https://stacx.mortgageconnectlp.com/ImportProject/UpdateChecklistOnOrder/182",
    "https://stacx.mortgageconnectlp.com/ImportProject/UpdateChecklistOnOrder/305",
    "https://stacx.mortgageconnectlp.com/ImportProject/UpdateChecklistOnOrder/310"
]

# Optional: Configure proxy if needed
# proxies = {
#     "http": "http://your.proxy.server:port",
#     "https": "http://your.proxy.server:port",
# }

# Fetch and print responses
for url in urls:
    try:
        # Add `proxies=proxies` if using a proxy
        response = requests.get(url)
        response.raise_for_status()
        print(f"Response from {url}:\n{response.text}\n{'-'*80}\n")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}:\n{e}\n{'-'*80}\n")
