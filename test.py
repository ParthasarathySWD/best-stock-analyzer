import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/aapl/prices?startDate=2024-05-12&token=0b80f5cbd9cefb1efedd03e05fd400cc3dd03862", headers=headers)
print(requestResponse.json())