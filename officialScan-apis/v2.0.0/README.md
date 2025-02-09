# **crypto-wallet-bruteforce v2.0.0**

`crypto-wallet-bruteforce` is an advanced tool designed to generate and brute-force crypto wallets, checking for any balances across multiple blockchain networks using public API services.

---

## **Disclaimer**

This script is developed for **educational and research purposes only**.

**By using this code, you agree to the following terms:**

1. **No Malicious Use:** You will not use this script for unauthorized access or malicious purposes.
2. **Explicit Permission:** You will obtain explicit permission before using this script on any system or network.
3. **Understand Risks:** You understand the implications of using such a tool, including potential legal consequences.
4. **No Liability:** The creators of this tool are not responsible for any misuse or consequences resulting from the use of this script.

**If you do not agree to these terms, please refrain from using this script.**

---

## **What's New in v2.0.0?**

- **Async API Requests:** Now utilizes asynchronous requests with `aiohttp` for faster wallet balance checks.
- **Explorer API Support:** Integrated support for BscScan, EtherScan, PolygonScan, and TronScan API.
- **Dynamic Configuration:** Interactive setup to configure API keys, network selection, and mnemonic settings.
- **Real-Time Progress Tracking:** Displays runtime statistics, API check times, and found balances in real-time.
- **Enhanced Logging:** Automatically saves details of wallets with balances to the `found_wallets` directory.
- **Continuous Operation:** Runs indefinitely until manually stopped, ensuring continuous wallet generation and checking.

---

## **Requirements**

Ensure the following are ready before running the script:

1. **Stable Internet Connection**
2. **Python 3.8+** (Download from [Python Official Site](https://www.python.org/))
3. **4GB RAM Minimum** (8GB Recommended)
4. **API Keys for Blockchain Explorers:**
   - [BscScan](https://bscscan.com/) ([View Instructions](https://docs.bscscan.com/getting-started/viewing-api-usage-statistics))
   - [EtherScan](https://etherscan.io/) ([View Instructions](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics))
   - [PolygonScan](https://polygonscan.com/) ([View Instructions](https://docs.polygonscan.com/getting-started/viewing-api-usage-statistics))
   - [TronScan](https://tronscan.org/) ([View Instructions](https://docs.tronscan.org/))

---

## **Getting Started**

### **1. Install Python**

Download and install Python from the official site:

```bash
https://www.python.org/downloads/
```

Ensure Python is added to your system’s PATH during installation.

### **2. Clone the Repository**

Use Git to clone the latest version of the repository:

```bash
git clone https://github.com/niyankhadka/crypto-wallet-bruteforce.git
```

`Note: Always look for latest release and use it.`
```
https://github.com/niyankhadka/crypto-wallet-bruteforce/releases
```

Navigate to the project directory:

```bash
cd crypto-wallet-bruteforce\officialScan-apis\v2.0.0\
```

### **3. Install Dependencies**

Run the following command to install the necessary libraries:

```bash
pip install -r requirements.txt
```

### **4. Obtain API Keys**

Create accounts and obtain API keys from the following platforms:

   - [BscScan](https://bscscan.com/) ([View Instructions](https://docs.bscscan.com/getting-started/viewing-api-usage-statistics))
   - [EtherScan](https://etherscan.io/) ([View Instructions](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics))
   - [PolygonScan](https://polygonscan.com/) ([View Instructions](https://docs.polygonscan.com/getting-started/viewing-api-usage-statistics))
   - [TronScan](https://tronscan.org/) ([View Instructions](https://docs.tronscan.org/))

### **5. Configure the Script**

Run the script to set up your configuration:

```bash
python main.py
```

You'll be prompted to:

- Select or create a new configuration setup.
- Choose the networks you want to scan.
- Enter the API keys for selected networks.
- Set mnemonic word count (12, 15, 18, 21, 24).
- Define how many addresses to generate per cycle (Derivation of address).

Once configured, the script will validate your settings and begin generating and checking wallets.

---

## **Running the Script**

To start the wallet brute-force process:

```bash
python main.py
```

The script will:

- Continuously generate mnemonics and derive wallet addresses.
- Check balances across the selected networks.
- Log wallet details with balances in the found_wallets directory.



### **Stopping the Script**

Press `Ctrl + C` to stop the script manually. It will display the total runtime and number of wallets found with balances.

---

## **Where to Find Discovered Wallets?**

### **Wallets with Balances**

All wallets with balances are saved in the `found_wallets/` directory with a timestamped filename, containing:

- The mnemonic phrase.
- Network name.
- Wallet address.
- Balance amount.

---

## **Limitations**

1. **API Rate Limits:** Free API keys may have rate limits. Upgrade to premium plans for higher limits.
2. **Supported Networks:** Currently supports BSC, Ethereum, Polygon, and Tron.
3. **Legal Considerations:** This tool should only be used in environments you own or have explicit permission to operate in.

---

## **Contribution**

Contributions are welcome! Feel free to:

- Submit issues if you encounter bugs.
- Open pull requests for enhancements or new features.

Your help in development, testing, and documentation is appreciated!

---

## **Donations**

If you find this tool helpful and would like to support further development, [Buy Me A Coffee](https://buymeacoffee.com/niyankhadka/).

---

## **License**

This project is licensed under the GPL-3.0 License.

[View License](https://github.com/niyankhadka/crypto-wallet-bruteforce/blob/main/LICENSE)

---

## **Acknowledgements**

Special thanks to:

   - [bip_utils](https://github.com/ebellocchia/bip_utils/) for powerful HD wallet functionalities.
   - [aiohttp](https://github.com/aio-libs/aiohttp/) for enabling efficient asynchronous HTTP requests.

---

`⭐ If you find this project useful, don't forget to star the repository and follow for updates! ⭐`