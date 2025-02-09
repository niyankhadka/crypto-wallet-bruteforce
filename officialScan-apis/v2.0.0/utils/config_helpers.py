import configparser
import os
from bip_utils import Bip44Coins


def get_active_config_path():
    """
    Get the path to the currently active configuration file.

    :return: Path to the active configuration file.
    """
    active_config_file = os.path.join("config_setups", "active_setup.ini")

    if os.path.exists(active_config_file):
        with open(active_config_file, "r") as file:
            config_path = file.read().strip()
            if os.path.exists(config_path):
                return config_path
            else:
                print(f"❌ Active config path in 'active_setup.ini' is invalid: {config_path}")

    raise FileNotFoundError("❌ No active configuration file found. Please set up the environment first.")


def load_config():
    """
    Load configuration settings from the active configuration file.

    :return: ConfigParser object for the active configuration.
    """
    config_path = get_active_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_word_count():
    return int(load_config()["DEFAULT"].get("MNEMONIC_WORD_COUNT", "12"))


def get_address_count():
    return int(load_config()["DEFAULT"].get("ADDRESS_COUNT", "1"))


def get_mnemonic_settings():
    return get_word_count(), get_address_count()


def get_selected_networks():
    config = load_config()
    selected_networks = {}
    for provider in config["DEFAULT"]["API_PROVIDERS"].split(","):
        networks = config["DEFAULT"].get(f"{provider}_NETWORKS", "").split(",")
        selected_networks[provider] = [network.strip() for network in networks]
    return selected_networks


def get_supported_networks():
    return {
        'Bip44': {
            "bsc": Bip44Coins.BINANCE_SMART_CHAIN,
            "ethereum": Bip44Coins.ETHEREUM,
            "polygon": Bip44Coins.POLYGON,
            "tron": Bip44Coins.TRON,
        }
    }


def get_api_keys(provider):
    config = load_config()
    if provider not in config:
        return {}
    return {key: value.strip() for key, value in config[provider].items()}
