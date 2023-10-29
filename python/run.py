# -------------------------------------
# Program Starts from here
# ------------------------------------- 

import os
import configparser
import json
import time
from datetime import date
import requests as req # pip install requests
from hdwallet import BIP44HDWallet # pip install hdwallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional 

# read config file
config = configparser.ConfigParser()
config.read('config.ini')

check_mainnet = ['bsc', 'eth', 'matic']

def mainnet_url( mainnet ):
    if mainnet == "bsc":
        mainnet_url = "https://api.bscscan.com/"
    elif mainnet == "eth":
        mainnet_url = "https://api.etherscan.io/"
    elif mainnet == "matic":
        mainnet_url = "https://api.polygonscan.com/"
    else:
        mainnet_url = "https://api.bscscan.com/"
    return mainnet_url

def mainnet_api( mainnet ):
    mainnet_api = config['api'][mainnet]
    return mainnet_api

def req_trnx( mainnet, address ):
    mainnet_url_link = mainnet_url( mainnet )
    mainnet_api_key = mainnet_api( mainnet )
    module = "account"
    action = "txlist"
    page_no = 1
    display_per_page = 1
    sort = "desc"
    trnx_response = req.get(f"{mainnet_url_link}api?module={module}&action={action}&address={address}&page={page_no}&offset={display_per_page}&sort={sort}&apikey={mainnet_api_key}", timeout = None)
    if trnx_response:
        trnx_info = trnx_response.json()
        return trnx_info
    
def req_balance( mainnet, address ):
    mainnet_url_link = mainnet_url( mainnet )
    mainnet_api_key = mainnet_api( mainnet )
    module = "account"
    action = "balance"
    balance_response = req.get(f"{mainnet_url_link}api?module={module}&action={action}&address={address}&apikey={mainnet_api_key}", timeout = None)
    if balance_response:
        balance_info = balance_response.json()
        return balance_info

# path of the directory
hasBalancePath = "hasBalance"

# creating the date object of today's date
todays_date = date.today()

looper_count = 0
fount_count = 0
looper = True
while looper:

    print(f"Total Checked: {looper_count} || Found: {fount_count}")

    # Generate english mnemonic words
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    # Secret passphrase/password for mnemonic
    PASSPHRASE: Optional[str] = None

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    print("Checking Mnemonic:", bip44_hdwallet.mnemonic())

    # Get Ethereum BIP44HDWallet information's from address index
    for address_index in range(1):
        # Derivation from Ethereum BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
        )
        # Drive Ethereum BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Print address_index, path, address and private_key
        # print(f"{bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()}")
        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()

        print(f"Wallet Address: {bip44_hdwallet.address()}" )

        for mainnet in check_mainnet:
            wallet_trnx_status = req_trnx( mainnet, bip44_hdwallet.address() )
            print(f"---- Checking Transaction(s) on {mainnet}")
            if wallet_trnx_status["status"] == "1":
                print(f"-------- Checking Balance on {mainnet}")
                wallet_trnx_balance = req_balance( mainnet, bip44_hdwallet.address() )
                if wallet_trnx_balance["result"] != "0":
                    fount_count+= 1
                    print(f"************ Found Balance on {mainnet}")
                    with open(r"{}\hasBalance-{}.txt".format(hasBalancePath, todays_date), "a") as hb:
                        hb.write( mainnet )
                        hb.write( " - " )
                        hb.write( wallet_trnx_balance["result"] )
                        hb.write( " || Mnemonic : " )
                        hb.write( bip44_hdwallet.mnemonic() )
                        hb.write( " || " )
                        hb.write( bip44_hdwallet.address() )
                        hb.write( " " )
                        hb.write( '\n' )
                        hb.close()
                else :
                    print(f"xxxxxxxx Not Found Balance on {mainnet}")
            else:
                print(f"xxxxxxxx No Transactions Found on {mainnet}")
        
    looper_count+= 1
    os.system('cls')
