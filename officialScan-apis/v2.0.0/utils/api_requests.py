import aiohttp
import asyncio
import os
from datetime import datetime
from utils import get_api_keys


async def fetch_balance(session, url, headers):
    """Perform an asynchronous GET request to fetch balance."""
    async with session.get(url, headers=headers) as response:
        return await response.json()


async def check_balance(session, network, address, api_key):
    """Check balance for a given network and address."""
    api_urls = {
        "bsc": f"https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey={api_key}",
        "ethereum": f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={api_key}",
        "polygon": f"https://api.polygonscan.com/api?module=account&action=balance&address={address}&apikey={api_key}",
        "tron": f"https://apilist.tronscanapi.com/api/account/token_asset_overview?address={address}",
    }

    headers = {}
    if network == "tron":
        headers["TRON-PRO-API-KEY"] = api_key  # Tron requires this header

    url = api_urls.get(network)
    if not url:
        print(f"❌ Unsupported network: {network}")
        return None

    try:
        response = await fetch_balance(session, url, headers)
        return process_balance_response(network, address, response)
    except Exception as e:
        print(f"⚠️  Error checking balance for {network} address {address}: {e}")
        return None


def process_balance_response(network, address, response):
    """Process the API response to extract balance."""
    if network == "tron":
        # Tron-specific response handling
        data = response.get("data", [])
        if data:
            for asset in data:
                if asset.get("tokenAbbr") == "trx" and int(asset.get("balance", 0)) > 0:
                    balance = int(asset["balance"]) / 1_000_000  # Convert from Sun to TRX
                    print(f"💰 Balance found for {address} on Tron: {balance} TRX")
                    return {"network": "tron", "address": address, "balance": balance}
        return None  # No balance found for Tron
    else:
        # EVM (Ethereum, BSC, Polygon) response handling
        balance_wei = int(response.get("result", 0))
        if balance_wei > 0:
            balance = balance_wei / 1e18  # Convert Wei to Ether
            print(f"💰 Balance found for {address} on {network.capitalize()}: {balance}")
            return {"network": network, "address": address, "balance": balance}
        return None  # No balance found


async def run_checks(derived_addresses, mnemonic):
    """Run balance checks for all derived addresses asynchronously."""
    api_keys = get_api_keys("ExplorerAPI")
    tasks = []

    async with aiohttp.ClientSession() as session:
        for network, addresses in derived_addresses.get("Bip44", {}).items():
            api_key = api_keys.get(f"{network}_key")
            for address in addresses:
                tasks.append(check_balance(session, network, address, api_key))
        print(f"✅ Checking {len(tasks)} addresses for balance...")
        # Execute all balance checks concurrently
        results = await asyncio.gather(*tasks)

    # Filter out None results (addresses with zero balance)
    found_balances = [result for result in results if result]

    if found_balances:
        save_balances(found_balances, mnemonic)
        return True
    else:
        return False


def save_balances(balances, mnemonic):
    """Save mnemonic and balance details to a file if balance is found."""
    if not os.path.exists("found_wallets"):
        os.makedirs("found_wallets")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"found_wallets/balance_found_{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(f"Mnemonic Phrase: {mnemonic}\n\n")
        file.write("Found Balances:\n")
        for balance_info in balances:
            file.write(f"Network: {balance_info['network'].capitalize()}, Address: {balance_info['address']}, "
                       f"Balance: {balance_info['balance']}\n")

    print(f"✅ Balance information saved to {filename}")