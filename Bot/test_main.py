import main
import datetime
import unittest
# run: "pytest"

data = []
portfolio = main.Positions()

def test_isLong():
    last_buy = datetime.datetime.now()
    price = 10
    portfolio.openTrade(True,price,1,last_buy)
    if portfolio.isLong(0) == True:
        assert True 

def test_isShort():
    last_buy = datetime.datetime.now()
    price = 10
    portfolio.openTrade(False,price,1,last_buy)
    if portfolio.isLong(0) == False:
        assert True
        
def test_multi_positions():
    last_buy = datetime.datetime.now()
    price = 10
    portfolio.openTrade(False,price,1,last_buy)
    portfolio.openTrade(True,price,1,last_buy)
    condition1 = portfolio.isLong(0) == False
    condition2 = portfolio.isLong(1) == True
    if condition1 and condition2:
        assert True

# def test_a():
    # OPEN_LONG = 1
    # CLOSE_LONG = 2
    # OPEN_SHORT = 3
    # CLOSE_SHORT = 4
    # data['Aroon down'][0] = 20
    # data['RSI'][0] = 20
    # Analysis.bearish(data)