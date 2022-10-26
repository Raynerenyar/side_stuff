import pandas_datareader as web
import talib
import numpy as np
from enum import Enum
import datetime
from .WalletManagement import make_trades, close_trades, rebalance_wallets, get_total_balance
from .StoreData.main import read_data_from_db, eth, dai
from .StoreData.UniswapData import get_uniswap_price
import sched, time
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=Warning)
import logging
logging.disable(logging.WARNING)
logging.disable(logging.INFO)



class PositionOptions(Enum):
    OPEN_LONG = 1
    CLOSE_LONG = 2
    OPEN_SHORT = 3
    CLOSE_SHORT = 4

class BuyOptions(Enum):
    INITIAL = 1
    DCA = 2


class Positions:
    
    def __init__(self, isLong, price, tvl_at_open, percent_fall=0):
        self.isLong = isLong
        self.price = price
        self.percent_fall = percent_fall
        self.tvl_at_open = tvl_at_open

    def longPosition(data):
        math = data['RSI'].iloc[-1] + data['Aroon down'].iloc[-1]
        if math < 70:
            return PositionOptions.OPEN_LONG
        elif math > 90:
            return PositionOptions.CLOSE_LONG
        
    def shortPosition(data):
        math = data['RSI'].iloc[-1] + data['Aroon down'].iloc[-1]
        if math > 130:
            return PositionOptions.OPEN_SHORT
        elif math > 110 or math < 130:
            return PositionOptions.CLOSE_SHORT
    

positions = []
pairIndex = 0
leverage = 5
take_profit = 0
stop_loss = 15
slippage = 0.25
referrer = "0x786e22B4BF1ef3a73Be33dF36E61321CCddba345"
last_buy = datetime.datetime.now()-datetime.timedelta(minutes=15)
simulate = False

def bot(data, price):
    global last_buy, positions
    
    # Math
    data['Aroon down'], _ = talib.AROON(low=data["Close"].to_numpy(), timeperiod = 14, high=data["Close"].to_numpy())#, fillna = False)
    data['RSI'] = talib.RSI(data["Close"],timeperiod=5)
    price = price
    long = Positions.longPosition(data)
    short = Positions.shortPosition(data)


    # time calculations so last investment > 10 mins ago
    now = datetime.datetime.now()
    time_difference = (now - last_buy).total_seconds()

    # if we don't have any positions open yet
    if len(positions) == 0:
        if long == PositionOptions.OPEN_LONG:
            # open long position
            position = Positions(True, price, get_total_balance(), 0)
            positions.append(position)
            make_trades(position, pairIndex, price, True, leverage, take_profit, stop_loss, slippage, referrer)
            last_buy = datetime.datetime.now()
        else:
            if short == PositionOptions.OPEN_SHORT:
                # open short position
                position = Positions(False, price, get_total_balance(), 0)
                positions.append(position)
                make_trades(position, pairIndex, price, False, leverage, take_profit, stop_loss, slippage, referrer)
                last_buy = datetime.datetime.now()

    
    # if we have already multiple positions opened
    else:
        # price difference for DCA part
        price_difference = price - positions[0].price
        print(price_difference)

        isLong = positions[0].isLong
        if isLong:
            # Stop loss, Stop loss gets done automatically by Gains Trade. Howesver we need to delete the positions.
            s_l = False
            if price_difference < -1 * positions[0].price * 0.15:
                s_l = True

            # Close when market gets too bearish
            if long == PositionOptions.CLOSE_LONG or s_l:
                last_position = positions[-1]
                close_trades(last_position, pairIndex)
                last_buy = datetime.datetime.now()-datetime.timedelta(minutes=15)
                positions = []
            
            # DCA part
            if long == PositionOptions.OPEN_LONG and (time_difference>60*10 or simulate): # check if price moved in wrong direction
                if price_difference < -1 * positions[0].price * (positions[-1].percent_fall+1)/100 and positions[-1].percent_fall < 10:
                    # DCA, open another position
                    position = Positions(True, price, positions[0].tvl_at_open, positions[-1].percent_fall+1)
                    positions.append(position)
                    make_trades(position, pairIndex, price, True, leverage, take_profit, stop_loss, slippage, referrer)
                    last_buy = datetime.datetime.now()


        else:

            # Stop loss
            s_l = False
            if price_difference > positions[0].price * 0.15:
                s_l = True

            #Close when markets get too bulish
            if short == PositionOptions.CLOSE_SHORT or s_l:
                last_position = positions[-1]
                close_trades(last_position, pairIndex)
                last_buy = datetime.datetime.now()-datetime.timedelta(minutes=15)
                positions = []

            # DCA part
            if short == PositionOptions.OPEN_SHORT and (time_difference>60*10 or simulate):
                if price_difference > position[0].price * (position[-1].percent_fall+1)/100 and position[-1].percent_fall < 10:
                    # DCA, open another position
                    position = Positions(False, price, positions[0].tvl_at_open, positions[-1].percent_fall+1)
                    positions.append(position)
                    make_trades(position, pairIndex, price, False, leverage, take_profit, stop_loss, slippage, referrer)
                    last_buy = datetime.datetime.now()
            
    

def main():
    # To simulate use read_data_from_db of the DATA Generator function
    if simulate:
        # Needs to be replaced by something better
        data = read_data_from_db(10000)
        data = pd.DataFrame(data, columns=["Close", "Time"])
        for i in range(600):
            data_ = data[i*15:(i+1)*15]
            bot(data_, data_["Close"])  

    else:
        # Does all the calculations every minute
        s = sched.scheduler(time.time, time.sleep)

        def main_func(sc):
            
            data = read_data_from_db(15)
            data.reverse()
            data = pd.DataFrame(data, columns=["Close", "Time"])
            price = get_uniswap_price(eth, dai)
            bot(data, price)
        
            sc.enter(60, 1, main_func, (sc,))

        s.enter(60, 1, main_func, (s,))
        s.run()
        
