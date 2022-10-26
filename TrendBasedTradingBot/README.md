
How to set up?

1. Install all required packages
1.1 Add a .env file with 4 private keys
2. Run scripts/StoreData/InitializeDB.py   # to initialize the DB
3. Run scripts/StoreData/main.py # this stores the price of a specific crypto in a DB, updates every 24 hours for the indicators, needs to run all the time.
4. Run scripts/Bot.py with brownie # main bot
