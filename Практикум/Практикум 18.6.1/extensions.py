import requests
import json

class APIException(Exception): pass
class Cryptoconverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        total_baase = json.loads(r.content)[base] * int(amount)
        return total_baase

    @staticmethod
    def convert(quote: str, base: str, amount: str, keys:dict):
        if quote == base : raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try: keys[quote]
        except KeyError: raise APIException(f'Не удалось обработать валюту {quote}')

        try: keys[base]
        except KeyError: raise APIException(f'Не удалось обработать валюту {base}')

        try: amount = float(amount)
        except ValueError: raise APIException(f'Не удалось обработать количество {amount}')        


        return Cryptoconverter.get_price(keys[quote], keys[base], amount)
