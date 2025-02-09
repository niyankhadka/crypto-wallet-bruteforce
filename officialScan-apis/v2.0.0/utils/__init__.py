# utils/__init__.py

from .console_helpers import ( 
    clear_console, 
    print_status, 
    print_separator 
)
from .network import wait_for_internet
from .config_helpers import (
    get_active_config_path,
    load_config,
    get_word_count,
    get_address_count,
    get_mnemonic_settings,
    get_selected_networks,
    get_supported_networks,
    get_api_keys,
)
from .mnemonic_generator import ( 
    generate_mnemonic, 
    generate_seed, 
    derive_addresses, 
    print_derived_addresses 
)
from .api_requests import run_checks

UTILS_VERSION = "1.0.0"