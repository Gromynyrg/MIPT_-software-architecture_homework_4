from converters import *


def main():
    amount = float(input('Введите значение в USD: '))

    converters = {
        "RUB": UsdRubConverter(),
        "EUR": UsdEurConverter(),
        "GBP": UsdGbpConverter(),
        "CNY": UsdCnyConverter()
    }

    for currency, converter in converters.items():
        result = converter.convert(amount, currency)
        if result is not None:
            print(f"{amount:.2f} USD → {result:.2f} {currency}")
        else:
            print(f"Ошибка конвертации в {currency}")


if __name__ == "__main__":
    main()
