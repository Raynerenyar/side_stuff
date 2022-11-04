
import requests
import json


def get_uniswap_price(token1, token2):
    response_API = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json["USD"]

