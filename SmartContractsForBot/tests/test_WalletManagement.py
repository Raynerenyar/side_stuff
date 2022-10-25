import pytest
from scripts.WalletManagement import get_balances, rebalance_wallets
from brownie import GNSTradingV6_2, config, accounts, Contract, GNSDaiTokenV5
import time


trading_v6_testnet = "0x81465dF3c64B18b4092990eB73200A3814AF75E5"
gfarm_dai = "0x04B2A6E51272c82932ecaB31A5Ab5aC32AE168C3"

account1 = accounts.add(config["wallets"]["wallet1"])
account2 = accounts.add(config["wallets"]["wallet2"])
account3 = accounts.add(config["wallets"]["wallet3"])
account4 = accounts.add(config["wallets"]["wallet4"])

our_accounts = [account1, account2, account3, account4]

def test_rebalance_wallets():
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    tx = gnsDaiTokenV5.transfer(account2, 5000*10**18, {"from":account1})
    tx.wait()
    balances = get_balances()
    assert balances[1]+5000 == balances[0]
    rebalance_wallets()
    balances = get_balances()
    assert balances[1] == balances[0]