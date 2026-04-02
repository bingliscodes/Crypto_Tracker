from abc import ABC, abstractmethod


# Will need to switch both URLs and headers, then handle responses differently based on source
# --- Strategy interface ---
class CryptoSourceStrategy(ABC):
    @abstractmethod
    def fetch_price(self, symbol: str) -> dict:
        pass


# --- Concrete Strategies ---
class CoinGeckoStrategy(CryptoSourceStrategy):
    def fetch_price(self, symbol: str) -> dict:
        # Make an API call to the CoinGecko API and return a standardized object with symbol, price, currency, and timestamp
        pass


class CoinMarketCapStrategy(CryptoSourceStrategy):
    def fetch_price(self, symbol: str) -> dict:
        pass


# --- Context ---
class CryptoDataFetcher:
    def __init__(self):
        self._crypto_source_strategy: CryptoSourceStrategy | None = None

    def set_strategy(self, strategy: CryptoSourceStrategy):
        self._crypto_source_strategy = strategy

    def get_price(self, symbol: str) -> dict:
        if self._crypto_source_strategy is None:
            return "Please set a strategy before retrieving data!"

        return self._crypto_source_strategy.fetch_price(symbol)
