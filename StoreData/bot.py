#%%
import pandas_datareader as web
import matplotlib.pyplot as plt
from ta.trend import AroonIndicator
from ta.momentum import RSIIndicator


class positions:
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
    
def main():
    # Load data
    data = web.DataReader("AAPL","yahoo")

    # Initialize Aroon Indicator
    indicatorAroon = AroonIndicator(close=data["Close"], window = 14, fillna = False)
    #Intialise RSI-5 (period is 5)
    indicatorRSI = RSIIndicator(data["Close"],5,False)

    # Aroon up is bullish if close to 100
    # Aroon up is bearish if close to 0
    # vice versa for Aroon down
    data['Aroon down'] = indicatorAroon.aroon_down()
    data['Aroon up'] = indicatorAroon.aroon_up()
    data['RSI'] = indicatorRSI.rsi()

    print(data)
    plt.plot(data['Aroon up'])
    plt.plot(data['Aroon down'])
    plt.show
    print(positions.isLongOpened)

if __name__ == "__main__":
    main()
    
#%%
