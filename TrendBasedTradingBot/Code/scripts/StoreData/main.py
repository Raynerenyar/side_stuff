from sqlalchemy import Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, desc, asc
import pathlib
import os
import datetime, time
#from .InitializeDB import Price, SQLALCHEMY_DATABASE_URI
import InitializeDB
import UniswapData
import sched

eth = "0x0000000000000000000000000000000000000000"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


def main():

    s = sched.scheduler(time.time, time.sleep)

    def main_func(sc):
        timestamp = datetime.datetime.now()
        price = UniswapData.get_uniswap_price(eth, dai)
        print(price)
        add_to_db(price, timestamp)
    
        sc.enter(60*60*24, 1, main_func, (sc,))

    s.enter(60*60*24, 1, main_func, (s,))
    s.run()
    


def add_to_db(price, timestamp, test=False):
    engine=None
    if test:
        engine = create_engine(InitializeDB.SQLALCHEMY_DATABASE_URI+"_test", echo=True)

    else:
        engine = create_engine(InitializeDB.SQLALCHEMY_DATABASE_URI, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    exchange_rate = InitializeDB.Price(price=price, time=timestamp, id=None)
    session.add(exchange_rate)
    session.commit()
    session.close()

# should give you x last data points back (sorted by date and time)
def read_data_from_db(x, test=False):
    engine=None
    if test:
        engine = create_engine(InitializeDB.SQLALCHEMY_DATABASE_URI+"_test", echo=True)

    else:
        engine = create_engine(InitializeDB.SQLALCHEMY_DATABASE_URI, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    price_data = [(x.price, x.time) for x in InitializeDB.Price.get_last_x_prices(session, x)]
    session.close()
    return price_data



if __name__ == "__main__":
    main()
    #print(read_data_from_db(10))
