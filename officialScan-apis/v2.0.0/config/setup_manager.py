import os
import subprocess
import configparser
from utils import get_supported_networks


def install_requirements():
    """Check and install missing packages from requirements.txt."""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt file not found.")
        return

    with open("requirements.txt", "r") as req_file:
        requirements = req_file.read().splitlines()

    for package in requirements:
        try:
            __import__(package.split("==")[0])  # Attempt to import the package
        except ImportError:
            print(f"⚠️  Installing missing package: {package}")
            subprocess.check_call(["pip", "install", package])

    print("✅ All required packages are installed.")


def set_active_config(config_path):
    """Save the selected configuration file path as active."""
    active_config_file = os.path.join("config_setups", "active_setup.ini")
    with open(active_config_file, "w") as file:
        file.write(config_path)


def setup_config():
    """Setup configuration for API keys, token networks, mnemonic, and address count."""
    config_folder = "config_setups"
    os.makedirs(config_folder, exist_ok=True)

    existing_setups = [f for f in os.listdir(config_folder) if f.endswith(".ini") and f != "active_setup.ini"]

    print("\n📂 Available setup options:")
    print("   0. ➕ Create a new setup")
    for i, setup in enumerate(existing_setups, 1):
        print(f"   {i}. {setup}")

    while True:
        choice = input("📂 Choose a setup to load or create a new one (enter the number): ").strip()
        try:
            choice = int(choice)
            if choice == 0:
                print("🆕 Creating a new setup.")
                break
            elif 1 <= choice <= len(existing_setups):
                config_path = os.path.join(config_folder, existing_setups[choice - 1])
                set_active_config(config_path)  # Save selected config as active
                print(f"✅ Loaded setup: {existing_setups[choice - 1]}")
                return config_path
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

    config_path = os.path.join(config_folder, input("🆕 Enter a name for the new setup file (e.g., explorer_setup.ini): ").strip())
    if not config_path.endswith(".ini"):
        config_path += ".ini"

    config = configparser.ConfigParser()
    config["DEFAULT"] = {"API_PROVIDERS": "ExplorerAPI"}

    # Fetch supported networks using get_supported_networks()
    explorer_networks = list(get_supported_networks()['Bip44'].keys())

    print("🌐 Available networks for ExplorerAPI:")
    for i, network in enumerate(explorer_networks, 1):
        print(f"   {i}. {network.capitalize()}")
    print("   all. Select all networks for ExplorerAPI")

    chosen_networks = []
    while True:
        network_choices = input("🌐 Enter the numbers of the networks you want to use (comma-separated, or 'all'): ").strip()
        if network_choices.lower() == "all":
            chosen_networks = explorer_networks
            break
        else:
            valid_selection = True
            for choice in network_choices.split(","):
                try:
                    selected_network = explorer_networks[int(choice) - 1]
                    if selected_network not in chosen_networks:
                        chosen_networks.append(selected_network)
                except (IndexError, ValueError):
                    print(f"❌ Invalid selection: {choice}")
                    valid_selection = False

            if valid_selection and chosen_networks:
                break
            print("❌ Invalid input. Please enter valid numbers or type 'all'.")

    config["DEFAULT"]["ExplorerAPI_NETWORKS"] = ",".join(chosen_networks)

    # Add API keys for each chosen network
    config["ExplorerAPI"] = {}
    for network in chosen_networks:
        while True:
            key = input(f"🔑 Enter the API key for {network} (cannot be empty): ").strip()
            if key:
                config["ExplorerAPI"][f"{network}_key"] = key
                break
            else:
                print(f"❌ API key for {network} is required. Please provide a valid key.")

    # Setup for mnemonic word count
    while True:
        try:
            word_count = int(input("👉 Enter the number of words for the mnemonic (12, 15, 18, 21, 24): "))
            if word_count not in [12, 15, 18, 21, 24]:
                raise ValueError("Word count must be one of 12, 15, 18, 21, 24.")
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    config["DEFAULT"]["MNEMONIC_WORD_COUNT"] = str(word_count)

    # Setup for number of addresses
    while True:
        try:
            num_addresses = int(input("👉 Enter the number of addresses to generate (minimum 1): "))
            if num_addresses < 1:
                raise ValueError("Number of addresses must be at least 1.")
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    config["DEFAULT"]["ADDRESS_COUNT"] = str(num_addresses)

    # Save configuration
    with open(config_path, "w") as config_file:
        config.write(config_file)

    set_active_config(config_path)  # Save new config as active
    print("✅ Configuration setup is complete.")
    return config_path


def validate_config(config_path):
    """Validate the configuration and add placeholders for missing or invalid values."""
    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run the setup first.")
        return False

    config = configparser.ConfigParser()
    config.read(config_path)

    config_updated = False
    all_valid = True

    # Validate mnemonic word count
    word_count = config["DEFAULT"].get("MNEMONIC_WORD_COUNT", "").strip()
    if word_count not in ["12", "15", "18", "21", "24"]:
        print("⚠️  Invalid or missing mnemonic word count. Setting default to 12.")
        config["DEFAULT"]["MNEMONIC_WORD_COUNT"] = "12"
        config_updated = True
        all_valid = False

    # Validate address count
    try:
        address_count = int(config["DEFAULT"].get("ADDRESS_COUNT", "0").strip())
        if address_count < 1:
            raise ValueError
    except ValueError:
        print("⚠️  Invalid or missing address count. Setting default to 1.")
        config["DEFAULT"]["ADDRESS_COUNT"] = "1"
        config_updated = True
        all_valid = False

    # Validate API keys and networks
    networks = config["DEFAULT"].get("ExplorerAPI_NETWORKS", "").split(",")
    missing_keys = []
    for network in networks:
        key_value = config["ExplorerAPI"].get(f"{network}_key", "<missing_key>").strip()
        if key_value in ("<missing_key>", ""):
            missing_keys.append(network)
            config["ExplorerAPI"][f"{network}_key"] = "<missing_key>"
            config_updated = True

    if missing_keys:
        print(f"⚠️  Missing API keys for ExplorerAPI: {', '.join(missing_keys)}")
        all_valid = False

    # Save updated configuration if any changes were made
    if config_updated:
        with open(config_path, "w") as config_file:
            config.write(config_file)
        print("⚠️  Configuration file updated with defaults.")

    if all_valid:
        print("✅ Configuration is valid.")
    else:
        print("❌ Configuration is incomplete. Please update placeholders in the config file.")

    return all_valid