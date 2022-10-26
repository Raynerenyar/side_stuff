from uniswap import Uniswap
from UniswapData import *
import pytest


# price of eth is bigger in the range of 1000 - 2000 rn, so this test might fail in the future
def test_get_price():
    price = get_uniswap_price()
    assert price < 2000 and price > 1000