from utils import ( 
    get_address_count, 
    get_selected_networks, 
    get_supported_networks
)
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip39WordsNum,
    Bip44,
    Bip44Coins,
    Bip44Changes
)


def get_words_num(word_count):
    """
    Map word count to Bip39WordsNum enumeration.

    :param word_count: Number of words in the mnemonic.
    :return: Corresponding Bip39WordsNum enumeration.
    """
    word_map = {
        12: Bip39WordsNum.WORDS_NUM_12,
        15: Bip39WordsNum.WORDS_NUM_15,
        18: Bip39WordsNum.WORDS_NUM_18,
        21: Bip39WordsNum.WORDS_NUM_21,
        24: Bip39WordsNum.WORDS_NUM_24,
    }
    return word_map.get(word_count, Bip39WordsNum.WORDS_NUM_12)


def generate_mnemonic(word_count):
    """
    Generate a mnemonic phrase.

    :param word_count: Number of words in the mnemonic.
    :return: Generated mnemonic phrase.
    """
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(get_words_num(word_count))
    print(f"✅ Mnemonic Generated: {mnemonic}")
    return mnemonic


def generate_seed(mnemonic):
    """
    Generate seed bytes from a mnemonic phrase.

    :param mnemonic: Mnemonic phrase.
    :return: Seed bytes.
    """
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    return seed_bytes


def derive_addresses(seed_bytes):
    """
    Derive addresses based on the provided seed bytes and configuration.

    :param seed_bytes: Seed bytes generated from the mnemonic.
    :return: Dictionary of derived addresses.
    """

    # Load configuration
    addr_num = get_address_count()  # Address count from config
    selected_networks = get_selected_networks()
    address_list = {}

    # Ensure only Bip44 is used
    for derivation_type, network_data in get_supported_networks().items():
        if derivation_type != "Bip44":
            continue  # Skip other types

        address_list[derivation_type] = {}

        for symbol, network in network_data.items():
            # Check if the network is selected in the config file
            if "ExplorerAPI" not in selected_networks or symbol not in selected_networks["ExplorerAPI"]:
                print(f"⚠️  Skipping {symbol} (Not selected in config)...")
                continue

            # Initialize the list for storing derived addresses
            address_list[derivation_type][symbol] = []

            try:
                # Construct from seed and derive the master context
                bip_mst_ctx = Bip44.FromSeed(seed_bytes, network)

                # Derive account and change contexts
                bip_acc_ctx = bip_mst_ctx.Purpose().Coin().Account(0)
                bip_chg_ctx = bip_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

                # Generate addresses
                for i in range(addr_num):
                    bip_addr_ctx = bip_chg_ctx.AddressIndex(i)
                    address = bip_addr_ctx.PublicKey().ToAddress()
                    address_list[derivation_type][symbol].append(address)
            except Exception as e:
                print(f"⚠️  Error deriving addresses for {symbol} ({derivation_type}): {e}")
    print(f"✅ All Addresses Generated.")
    return address_list


def print_derived_addresses(address_list):
    """
    Print the derived addresses in a structured format.

    :param address_list: Dictionary of derived addresses.
    """
    print("\n🎉 Derived Addresses:")
    for derivation_type, networks in address_list.items():
        print(f"\n🔗 {derivation_type}:")
        for network, addresses in networks.items():
            print(f"  🌐 {network.capitalize()}:")
            for idx, address in enumerate(addresses, 1):
                print(f"    {idx}. {address}")