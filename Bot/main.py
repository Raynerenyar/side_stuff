import pandas_datareader as web
import matplotlib.pyplot as plt
import talib
import numpy as np
from enum import Enum
import datetime


class PositionOptions(Enum):
    OPEN_LONG = 1
    CLOSE_LONG = 2
    OPEN_SHORT = 3
    CLOSE_SHORT = 4

class BuyOptions(Enum):
    INITIAL = 1
    DCA = 2


class Positions:
    
    def __init__(self, price):
        self.isLong = False
        self.price = None
        self.percent_fall = 0
    
    #isLongOpened = False

    # TODO: add position counter, entry, exit, PnL, size
    def longPosition(data):
        math = data['RSI'][-1] + data['Aroon down'][-1]
        if math < 70:
            return PositionOptions.OPEN_LONG
        # TODO: check if long position is opened
        elif math > 90:
            return PositionOptions.CLOSE_LONG
        
    def shortPosition(data):
        math = data['RSI'][-1] + data['Aroon down'][-1]
        if math > 130:
            return PositionOptions.OPEN_SHORT
        # TODO: check if short positions is opened
        elif math > 110 or math < 130:
            return PositionOptions.CLOSE_SHORT
    

positons = []
last_buy = None

def main():
    # Load data
    data = web.DataReader("AAPL","yahoo")

    data['Aroon down'], _ = talib.AROON(low=data["Close"], timeperiod = 14, high=np.zeros(data["Close"].shape))#, fillna = False)
    data['RSI'] = talib.RSI(data["Close"],timeperiod=5)
    price = data["Close"][-1]
    

    """print(data)
    plt.plot(data['Aroon down'])
    plt.plot(data['RSI'])
    plt.show()"""
    #print(position.longPosition(data))
    #print(position.shortPosition(data))
    #for p in positions:
    #    if p.isOpened:

    #Positions.longPosition()

    long = Positions.longPosition(data)
    short = Positions.shortPosition(data)
    now = datetime.datetime.now()
    time_difference = (now - last_buy).total_seconds()

    # if we don't have any positions open yet
    if len(positons) == 0:
        if long == PositionOptions.OPEN_LONG:
            # open long position
            last_buy = datetime.datetime.now()
            pass
        else:
            if short == PositionOptions.OPEN_SHORT:
                # open short position
                last_buy = datetime.datetime.now()
                pass
    # if we have already multiple positions opened
    else:
        # price difference
        price_difference = price - positons[0].price

        isLong = positons[0].isLong
        if isLong:
            # Close when market gets too bearish
            if long == PositionOptions.CLOSE_LONG:
                # Close all positions
                pass
            
            # DCA part
            if long == PositionOptions.OPEN_LONG and time_difference>60*10: # check if price moved in wrong direction
                if price_difference < -1 * position[0].price * (position[-1].percent_fall+1) and position[-1].percent_fall < 10:
                    # DCA, open another position
                    pass


        else:
            #Close when markets get too bulish
            if short == PositionOptions.CLOSE_SHORT:
                # Close all positions
                pass

            # DCA part
            if short == PositionOptions.OPEN_SHORT and time_difference>60*10:
                if price_difference > position[0].price * (position[-1].percent_fall+1) and position[-1].percent_fall < 10:
                    # DCA, open another position
                    pass
            
    

if __name__ == "__main__":
    #positons = []
    while True:
        main()
            
