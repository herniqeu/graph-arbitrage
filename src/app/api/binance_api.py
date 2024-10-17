import requests

def get_all_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    pairs = [s['symbol'].lower() for s in data['symbols']]
    return pairs