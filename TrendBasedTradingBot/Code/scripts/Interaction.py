from brownie import GNSTradingV6_2, config, accounts, Contract
import time


trading_v6_testnet = "0x81465dF3c64B18b4092990eB73200A3814AF75E5"
my_account = "0xc0Ea5c77570efDD46911436bdb295cAc57720a31"

# asset pairIndex from gains network, price of the asset, leverage as an int 10 for 10x leverage, take_profit in percent,  stop_loss in percent, slippage, position size in DAI
def open_trade(account, pairIndex, price, position_size, buy_trade, leverage, take_profit, stop_loss, slippage, referrer=my_account):
    gnstradingv6 = GNSTradingV6_2.at(trading_v6_testnet)
    """
    opens a trade on gains network
    1. t(tuple): (your address[doesn't really matter because address gets autofilled], pairIndex https://gains-network.gitbook.io/docs-home/gtrade-leveraged-trading/pair-list,
    slot of the trade[will automatically use the first one that's open], initial position size[0 on new position], position size in DAI * 10**18, open price[10 decimal places 464203500000000 --> 46,420.35],
    buy Trade[true for long position, false for short], leverage, take_profit, stop_loss)
    2. order type: 0 for market, 1 for limit, 2 for stop limit
    3. spreadReductionId: not relevant, your NFT type to lower spread
    4. max allowed slippage
    5. referral address --> decreased fees and money for the referrer
    """
    price = price* 10**10
    slippage = slippage * 10**10
    if buy_trade:
        profit_price = price + (0.01 * price * take_profit/leverage)
        loss_price = price - (0.01 * price * (stop_loss/leverage))
    else:
        profit_price = price - (0.01 * price * take_profit/leverage)
        loss_price = price + (0.01 * price * (stop_loss/leverage))

    trade = gnstradingv6.openTrade([my_account, pairIndex, 0, 0, position_size*10**18, price, buy_trade, leverage, profit_price, loss_price], 0, 0,
    slippage, referrer, {"from": account})
    trade.wait(1)

    return trade.events



# Closing the trade at slot slot for the pairIndex
def close_trade(account, pairIndex, slot):
    gnstradingv6 = GNSTradingV6_2.at(trading_v6_testnet)
    print(gnstradingv6.isPaused())
    
    trade = gnstradingv6.closeTradeMarket(pairIndex, slot, {"from": account})
    trade.wait(1)
    
    return trade.events




def main():
    #open_trade(0, 19179.25*10**10, 1000, True, 10, 25, 10, 0.25*10**10, "0xE6dE2F8F6987202909bd2935dF459fe1Eb007122")
    #time.sleep(15)
    account = accounts.add(config["wallets"]["wallet1"])
    close_trade(0,0)
    close_trade(0,1)
    close_trade(0,2)