# SpaceDex

Here is the full doc: https://docs.google.com/document/d/1e49x2M588mvh8mIJqNMBjy29uPXEFzGnYnaRelKDFIY/edit

We only need to focus on the trend-based trading bot. This will be post-launch, so we have some time.


Gains network uses a special way(to avoid liquidations because of outliers etc.) to get their trading pair data. Although they probably should just have the same prices like Uniswap because the liquidity their should be really high.

So let's just use the Uniswap V3 price data. That's way cheaper. 


The StoreData package is already a working part of the bot. 

How to use?
1. Install the python packages...
uniswap-python, SQLAlchemy,
2. Run  InitializeDB.py, this one will create the SQLite DB and set it up. We will store our price data here.
3. Now you can run main. This will get the price data from uniswap of the ETH/DAI trading pair every minute and write it in the data base
