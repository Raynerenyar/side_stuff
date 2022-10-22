import pandas_datareader as web
import matplotlib.pyplot as plt
import talib
import numpy as np

class Positions:
    isShortOpened = False
    isLongOpened = False

    # TODO: add position counter, entry, exit, PnL, size
    def longPosition(self, data):
        math = data['RSI'][-1] + data['Aroon down'][-1]
        if math < 70:
            return 'open long'
        # TODO: check if long position is opened
        elif math > 90 and self.isLongOpened:
            return 'close long'
        
    def shortPosition(self, data):
        math = data['RSI'][-1] + data['Aroon down'][-1]
        if math > 130:
            return 'open short'
        # TODO: check if short positions is opened
        elif math > 110 or math < 130 and self.isShortOpened:
            return 'close short'
    
def main(position):
    # Load data
    data = web.DataReader("AAPL","yahoo")

    data['Aroon down'], _ = talib.AROON(low=data["Close"], timeperiod = 14, high=np.zeros(data["Close"].shape))#, fillna = False)
    data['RSI'] = talib.RSI(data["Close"],timeperiod=5)
    
    """print(data)
    plt.plot(data['Aroon down'])
    plt.plot(data['RSI'])
    plt.show()"""
    print(position.longPosition(data))
    print(position.shortPosition(data))

    

if __name__ == "__main__":
    position = Positions()
    while True:
        main(position)
        