from uniswap import Uniswap

address = None          # or None if you're not going to make transactions
private_key = None  # or None if you're not going to make transactions
version = 3                       # specify which version of Uniswap to use
provider = "https://mainnet.infura.io/v3/66c5cf5015244de0959f331f72cd29ab"    # can also be set through the environment variable `PROVIDER`
uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)



def get_uniswap_price(token1_address, token2_address):
    return uniswap.get_price_input(token1_address, token2_address, 10**18)/10**18