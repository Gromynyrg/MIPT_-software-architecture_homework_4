import requests
import json
import time
import os
import logging


class RateProvider:
    def __init__(
        self,
        api_url: str = "https://api.exchangerate-api.com/v4/latest/USD",
        cache_file: str = "exchange_rates.json",
        cache_expiry: int = 3600,
        max_retries: int = 3,
        retry_delay: int = 2
    ):
        self.api_url = api_url
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_from_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    if time.time() - data['timestamp'] < self.cache_expiry:
                        return data['rates']
            except (json.JSONDecodeError, KeyError, IOError):
                self.logger.warning("Invalid or corrupted cache file.")
        return None

    def _save_to_cache(self, rates: dict):
        try:
            data = {'timestamp': time.time(), 'rates': rates}
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            self.logger.error(f"Cache save failed: {e}")

    def get_rates(self) -> dict | None:
        rates = self._load_from_cache()
        if rates:
            return rates

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.api_url, timeout=5)
                response.raise_for_status()
                rates = response.json()['rates']
                self._save_to_cache(rates)
                return rates
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Data parsing error: {e}")
                return None
        return None
