from re import I
import pandas_datareader as web
import talib
import numpy as np
from enum import Enum
import datetime
# import matplotlib.pyplot as plt
import pdb


class PositionOptions(Enum):
    OPEN_LONG = 1
    CLOSE_LONG = 2
    OPEN_SHORT = 3
    CLOSE_SHORT = 4

class BuyOptions(Enum):
    INITIAL = 1
    DCA = 2


class Positions:
    
    def __init__(self):
        self.positionArr = []
    
    # add trade into portfolio    
    def openTrade(self, isLong, price, size, time):
        self.positionArr.append(Trade(isLong, price, size, time))
        print("trade opened")
        return "trade opened"
    
    # rm trade from portfolio
    def closeTrade(self,index):
        self.positionArr.pop(index)
        print("trade closed")
        return "trade closed"
    
    def price(self, index):
        return self.positionArr[index].price
    
    def isLong(self, index):
        return self.positionArr[index].isLong
    
    def time(self, index):
        return self.positionArr[index].time
        
    def __len__(self):
        return len(self.positionArr)
    
class Trade:
    
    def __init__(self,isLong, price, size, time):
        self.isLong = isLong
        self.price = price
        self.size = size
        self.time = time
        self.percent_fall = 0
        

class Analysis:
    def bullish(data):
        math = data['RSI'][-1] + data['Aroon down'][-1]
        if math < 70:
            return PositionOptions.OPEN_LONG.value
        elif math > 90:
            return PositionOptions.CLOSE_LONG.value
        
    def bearish(data):
        math = data['RSI'][-1] + data['Aroon down'][-1]
        if math > 130:
            return PositionOptions.OPEN_SHORT.value
        elif math > 110 or math < 130:
            return PositionOptions.CLOSE_SHORT.value

portfolio = Positions()

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
    #print(position.bullish(data))
    #print(position.bearish(data))
    #for p in positions:
    #    if p.isOpened:

    long = Analysis.bullish(data)
    short = Analysis.bearish(data)
    now = datetime.datetime.now()
    portfolioPositionCount = len(portfolio)
    #testing
    short = 3

    # if we don't have any positions open yet
    if portfolioPositionCount == 0:
        if long == PositionOptions.OPEN_LONG.value:
            # open long position
            last_buy = datetime.datetime.now()
            portfolio.openTrade(True,price,1,last_buy)
            pass
        else:
            if short == PositionOptions.OPEN_SHORT.value:
                # open short position
                last_buy = datetime.datetime.now()
                portfolio.openTrade(False,price,1,last_buy)
                pdb.set_trace()
                pass
            
    # if we have already multiple positions opened
    else:
        # for each position currently opened
        for i in range(0, portfolioPositionCount):
            # price difference
            price_difference = price - portfolio.price(i)
            time_difference = (now - last_buy).total_seconds()
            isLong = portfolio.isLong(i)
            if isLong:
                # Close when market gets too bearish
                if long == PositionOptions.CLOSE_LONG.value:
                    # Close all positions
                    portfolio.closeTrade(i)
                    pass
                
                # DCA part
                if long == PositionOptions.OPEN_LONG.value and time_difference>60*10: # check if price moved in wrong direction
                    if price_difference < -1 * portfolio.price(i) * (portfolio.positionArr[-1].percent_fall+1) and portfolio.positionArr[i].percent_fall < 10:
                        # DCA, open another position
                        last_buy = datetime.datetime.now()
                        portfolio.openTrade(True,price,1,last_buy)
                        pass


            else:
                #Close when markets get too bulish
                if short == PositionOptions.CLOSE_SHORT.value:
                    # Close all positions
                    portfolio.closeTrade(i)
                    pass

                # DCA part
                if short == PositionOptions.OPEN_SHORT.value and time_difference>60*10:
                    if price_difference > portfolio.price(1) * (portfolio.positionArr[i].percent_fall+1) and portfolio.positionArr[I].percent_fall < 10:
                        # DCA, open another position
                        last_buy = datetime.datetime.now()
                        portfolio.openTrade(False,price,1,last_buy)
                        pass
            
    

if __name__ == "__main__":
    #positions = []
    while True:
        main()
            
