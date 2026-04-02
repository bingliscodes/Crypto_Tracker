from abc import ABC, abstractmethod
from datetime import datetime, timezone
from .get_data import get_coingecko_data, get_coinmarketcap_data


# Will need to switch both URLs and headers, then handle responses differently based on source
# --- Strategy interface ---
class FetchStrategy(ABC):
    @abstractmethod
    def fetch_all_prices(self) -> list[dict]:
        pass

    @abstractmethod
    def fetch_price(self, symbol: str) -> dict:
        pass


# --- Concrete Strategies ---
class CoinGeckoStrategy(FetchStrategy):
    def fetch_all_prices(self):
        return get_coingecko_data()

    def fetch_price(self, symbol: str) -> dict:
        # Make an API call to the CoinGecko API and return a standardized object with symbol, price, currency, and timestamp
        pass


class CoinMarketCapStrategy(FetchStrategy):
    def fetch_all_prices(self):
        return get_coinmarketcap_data()

    def fetch_price(self, symbol: str) -> dict:
        pass


class MockStrategy(FetchStrategy):
    def fetch_all_prices(self) -> list[dict]:
        return [
            {
                "name": "Bitcoin",
                "symbol": "btc",
                "price": 10000,
                "timestamp": datetime.now(timezone.utc),
                "currency": "USD",
            },
            {
                "name": "CannoliCoin",
                "symbol": "ctc",
                "price": 999999,
                "timestamp": datetime.now(timezone.utc),
                "currency": "USD",
            },
        ]

    def fetch_price(self, symbol: str) -> dict:
        return (
            {
                "name": "Bitcoin",
                "symbol": "btc",
                "price": 10000,
                "timestamp": datetime.now(timezone.utc),
                "currency": "USD",
            },
        )


# I think we can just use one context for everything?
# --- Context ---
class CryptoDataFetcher:
    def __init__(self):
        self._crypto_source_strategy: FetchStrategy | None = None

    def set_strategy(self, strategy: FetchStrategy):
        self._crypto_source_strategy = strategy

    def get_price(self, symbol: str) -> dict:
        if self._crypto_source_strategy is None:
            return "Please set a strategy before retrieving data!"

        return self._crypto_source_strategy.fetch_price(symbol)
