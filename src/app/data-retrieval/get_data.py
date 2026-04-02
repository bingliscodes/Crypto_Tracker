import requests
from dotenv import load_dotenv
import os

load_dotenv()

# --- CoinGecko ---
# api_url = "https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0x2260fac5e5542a773aa44fbcfedf7c193bc2c599&vs_currencies=usd"
# Use coins/markets to get all coins with their id, symbol, name, and price
api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
headers = {"x-cg-pro-api-key": os.getenv("COINGECKO_API_KEY")}
response = requests.get(api_url, headers=headers)
print(response.json())
"""
Getting price requires the id (human readable name) and contract_address of a token.
Response format for coin:
{
  "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": {
    "usd": 67187.3358936566,
    "usd_market_cap": 1317802988326.25,
    "usd_24h_vol": 31260929299.5248,
    "usd_24h_change": 3.63727894677354,
    "last_updated_at": 1711356300
  }
}
"""
exit()
# --- CoinMarketCap ---
api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
headers = {
    "Accept": "application/json",
    "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
}
response = requests.get(api_url, headers=headers)
data = response.json()
print(data["data"][0]["quote"]["USD"])

# Can use /coins/list endpoint to get the symbol and contract addresses for all supported coins
