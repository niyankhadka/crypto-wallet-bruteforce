# crypto-wallet-bruteforce

Python based crypto wallet bruteforce script which is for educational purposes only. Use this script at your own risk. 

Script Requirements

    Here are the requirements that needs to be available before starting. 
    
    1. Very good internet connection and device (4/8GB RAM)
    2. Python Program available/insalled on machine
    3. GitHub (optional)
    4. Text Editor (VSCode, I preferred)
    5. BscScan API
    6. EtherScan API
    7. PolygonScan API

Getting Started:

    All you need is very good internet connection and few python libraries to be installed at the running device.

    Follow the below steps one by one if you are starting from scratch. For already experienced people, you know it. Just skip few steps and have a short glace at it.

    Let's get set go.........

    1. Install Python from official link (nake sure to use latest version)
    Link: https://www.python.org/

    2. After installation, download the crypto-wallet-bruteforce package as zip file. 
    Always look for latest release and use it.
    Link: https://github.com/niyankhadka/crypto-wallet-bruteforce/releases

    3. Unzip the file to your favourite drive folder.
        There are few steps that need to be done. Don't worry, explore more steps below.

    4. Create or login account to the following blockchain explorer

        a. BscScan API
        Link: https://bscscan.com/
        b. EtherScan API
        Link: https://etherscan.io/
        c. PolygonScan API
        Link: https://polygonscan.com/

    After creating or logging on acccounts on them, go to api keys where it can be seen from left side of your dashboard or from your profile menu. 
    Create new api keys for respective blockchain explorer. You can give 'Test' or any name you want as App Name.

    5. After creating accounts, get back to folder where you have save this file.

        a. Go to crypto-wallet-bruteforce/python 
        b. Open config.ini file
        c. Paste the copied API keys on respective name there.

    6. Now it's time to install the python libraries that needed to be installed to run the script. Just hang on, this one is the final setup process. Will try to make setup process easier on updates. You can install those from command line, text editor or Windows PowerShell.

    Copy and run following codes one by one:

        a. pip install requests
        b. pip install hdwallet

    Alright, initial setup process is completed. Now, we are ready to run the script.

Run Script:

    To run this script on this version, navigate to 'cd crypto-wallet-bruteforce\python\' and make sure you are on right path. 
    Type 'python run.py' and hit enter. 

    Now, the script will start to run and will display the updates on the screen. 

Check Successful Wallets:

    Navigate to crypto-wallet-bruteforce\python\hasBalance\ folder. There you can see all the wallets details which has amount on it. 

Limitations:

    1. API Keys are available on free and pro so, based on it, it depends upon how many scripts you want to run for this bruteforce process.
    2. For now, bsc, eth and matic is only supported. For other crypto currencies network, will update later on.
    3. It is the initial version of the script so, somewhere there might be missing or issue. If you are interested to contribute, we are open and really appreciated.

Thank Note:

    Thanks to https://github.com/meherett/python-hdwallet for the awesome python library you have created.

Contribution:

    Feel free to open an issue if you find a problem, or a pull request if you've solved an issue. And also any help in testing, development, documentation and other tasks is highly appreciated and useful to the project.

Donations:

    If You found this tool helpful consider making a donation, kindly contact me. (Will provide details on updates further)

License:
    This project is under GPL-3.0 license. 
    Link: https://github.com/niyankhadka/crypto-wallet-bruteforce/blob/main/LICENSE
