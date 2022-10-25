from brownie import GNSTradingV6_2, config, accounts, Contract, GNSDaiTokenV5
import time


trading_v6_testnet = "0x81465dF3c64B18b4092990eB73200A3814AF75E5"
gfarm_dai = "0x04B2A6E51272c82932ecaB31A5Ab5aC32AE168C3"

account1 = accounts.add(config["wallets"]["wallet1"])
account2 = accounts.add(config["wallets"]["wallet2"])
account3 = accounts.add(config["wallets"]["wallet3"])
account4 = accounts.add(config["wallets"]["wallet4"])

our_accounts = [account1, account2, account3, account4]

gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)

# approves DAI for all wallets
def approve_all(amount):
    for a in our_accounts:
        gnsDaiTokenV5.approve(trading_v6_testnet, amount, {"from": a})

# gets some testnet dai for each wallet
def get_testnet_dai():
    for a in our_accounts:
        gnsDaiTokenV5.getFreeDai({"from": a})


def get_total_balance():
    total_balance = 0
    for a in our_accounts:
        total_balance += gnsDaiTokenV5.balanceOf(a)
        #print(a)
    print(total_balance/10**18)
    return total_balance/10**18

def get_balances():
    return [gnsDaiTokenV5.balanceOf(a)/10**18 for a in our_accounts]

def rebalance_wallets():
    balances = get_balances()
    total_balace = 0
    for b in balances:
        total_balace += b
    
    for i, a in enumerate(our_accounts[1:]):
        if balances[i+1]> 0:
            tx = gnsDaiTokenV5.transfer(account1, balances[i+1]*10**18, {"from": a})
            tx.wait(1)
    for a in our_accounts[1:]:
        tx = gnsDaiTokenV5.transfer(a, total_balace/4 * 10**18, {"from": account1})
        tx.wait(1)
    print("Succesfully rebalanced wallets!")
    
#def buy_order():


def main():
    #approve_all(1000000000)
    #get_testnet_dai()
    rebalance_wallets()