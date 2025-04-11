from currency_converter import CurrencyConverter
from rate import RateProvider


class UsdGbpConverter(CurrencyConverter):
    def __init__(self, rate_provider: RateProvider = None):
        self.rate_provider = rate_provider or RateProvider()
        self.supported_currency = "GBP"

    def convert(self, amount: float, target_currency: str) -> float | None:
        if target_currency != self.supported_currency:
            self.rate_provider.logger.error(
                f"Unsupported currency: {target_currency}. "
                f"Supported: {self.supported_currency}"
            )
            return None

        if rates := self.rate_provider.get_rates():
            return amount * rates.get(self.supported_currency, 0)
        return None
