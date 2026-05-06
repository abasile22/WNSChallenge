import math

import requests


class Utils:

    @staticmethod
    def calculate_price(weight_grams, price_by_kilo):
        peso_ajustado = math.ceil(weight_grams / 250) * 250
        return (peso_ajustado / 1000) * price_by_kilo

    @staticmethod
    def get_ratio_by_date(date):
        response = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/usd.json")
        ratios = response.json()
        return ratios["usd"]["ars"]