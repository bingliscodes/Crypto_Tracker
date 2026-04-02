import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()


# --- CoinGecko ---
# api_url = "https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0x2260fac5e5542a773aa44fbcfedf7c193bc2c599&vs_currencies=usd"
# Use coins/markets to get all coins with their id, symbol, name, and price
def get_coingecko_data() -> list:
    api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    headers = {"x-cg-pro-api-key": os.getenv("COINGECKO_API_KEY")}
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


# TODO: Implement currency option


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


print(get_coinmarketcap_data())

# Can use /coins/list endpoint to get the symbol and contract addresses for all supported coins
