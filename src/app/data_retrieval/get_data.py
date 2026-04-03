import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()


# TODO: Implement currency option


# --- CoinGecko ---
def get_coingecko_data() -> list:
    api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    headers = {"x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")}
    response = requests.get(api_url, headers=headers)
    data = response.json()
    formatted_prices = []
    for coin in data:
        curr_coin = {
            "name": coin["name"],
            "symbol": coin["symbol"],
            "price": coin["current_price"],
            "timestamp": datetime.now(timezone.utc),
            "currency": "USD",
        }
        formatted_prices.append(curr_coin)

    return formatted_prices


def get_coingecko_price_by_symbol(symbol: str) -> dict:
    # I can't find an endpoint that lets me lookup by symbol, so I would have to make another API call anyway. Alternatively I could create
    # another API call that gets all currency, then only returns the specified one, but that still is the same amount of work as my current implementation
    api_url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&symbols={symbol}"
    headers = {"x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")}
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return data


print(get_coingecko_price_by_symbol("btc"))


# --- CoinMarketCap ---
def get_coinmarketcap_data() -> list:
    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
    }
    response = requests.get(api_url, headers=headers)
    json = response.json()
    data = json["data"]
    formatted_prices = []
    for coin in data:
        curr_coin = {
            "name": coin["name"],
            "symbol": coin["symbol"].lower(),
            "price": coin["quote"]["USD"]["price"],
            "timestamp": datetime.now(timezone.utc),
            "currency": "USD",
        }
        formatted_prices.append(curr_coin)
    return formatted_prices
