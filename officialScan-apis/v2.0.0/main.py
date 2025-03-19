import time
import asyncio
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count
from config import (
    install_requirements,
    setup_config,
    validate_config
)
from utils import (
    wait_for_internet,
    get_mnemonic_settings,
    generate_mnemonic,
    generate_seed,
    derive_addresses,
    run_checks,
    clear_console,
    print_status,
    print_separator
)

def wallet_generation_and_check():
    # Step 5: Extract mnemonic settings
    word_count, address_count = get_mnemonic_settings()

    # Step 6: Generate mnemonic
    mnemonic = generate_mnemonic(word_count)

    # Step 7: Generate seed bytes
    seed_bytes = generate_seed(mnemonic)

    # Step 8: Derive addresses
    derived_addresses = derive_addresses(seed_bytes)

    # Step 9: Check for internet again before API calls
    print_status("Re-checking internet connection before API requests...", symbol="🌐")
    wait_for_internet()

    # Step 10: Check balances and save if found
    api_start_time = time.time()
    balances_found = asyncio.run(run_checks(derived_addresses, mnemonic))
    api_end_time = time.time()
    last_api_check_duration = timedelta(seconds=(api_end_time - api_start_time))

    return balances_found

def worker_process(worker_id):
    checked_counter = 1
    script_start_time = time.time()
    last_check_duration = timedelta(0)
    last_api_check_duration = timedelta(0)
    last_balance_status = "No balance found"
    total_balances_found = 0

    print(f"\n🔁 Worker {worker_id} starting continuous wallet generation and balance checks... (Press Ctrl+C to stop)\n")

    try:
        while True:
            # Clear console before starting a new check
            clear_console()

            check_start_time = time.time()
            total_elapsed_time = timedelta(seconds=(check_start_time - script_start_time))

            # Display script runtime, last check info, API check time, and balance status at the top
            print_separator()
            print_status(f"Worker {worker_id} - Total Script Runtime: {total_elapsed_time}", symbol="⏱️")
            print_status(f"Worker {worker_id} - Checked {checked_counter} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", symbol="🔄")
            
            if checked_counter > 1:
                print_status(f"Worker {worker_id} - Previous Check {checked_counter - 1} completed in {last_check_duration}", symbol="✅")
                print_status(f"Worker {worker_id} - Previous API Check Time: {last_api_check_duration}", symbol="🌐")
                print_status(f"Worker {worker_id} - Previous Check Result: {last_balance_status}", symbol="💰")
                print_status(f"Worker {worker_id} - Total Balances Found So Far: {total_balances_found}", symbol="📊")
            print_separator()

            # Run wallet generation and balance check
            balances_found = wallet_generation_and_check()

            # Update balance status and total count
            if balances_found:
                last_balance_status = "Balance Found!"
                total_balances_found += 1
            else:
                last_balance_status = "No balance found"

            # Track overall check timing
            check_end_time = time.time()
            last_check_duration = timedelta(seconds=(check_end_time - check_start_time))

            # Increment checked counter for the next iteration
            checked_counter += 1

    except KeyboardInterrupt:
        print_status(f"Worker {worker_id} manually stopped by user.", symbol="🛑")
        total_run_time = timedelta(seconds=(time.time() - script_start_time))
        print_status(f"Worker {worker_id} - Total script runtime: {total_run_time}", symbol="⏱️")
        print_status(f"Worker {worker_id} - Total balances found during the session: {total_balances_found}", symbol="📊")

def get_user_core_input():
    """Prompt the user to input the number of CPU cores to use."""
    try:
        user_input = input(f"Enter the number of CPU cores to use (1-{cpu_count()}): ").strip()
        if user_input == "":
            print("No input provided. Defaulting to 1 CPU core.")
            return 1
        num_cores = int(user_input)
        if num_cores < 1 or num_cores > cpu_count():
            print(f"Input out of range. Defaulting to 1 CPU core.")
            return 1
        return num_cores
    except ValueError:
        print("Invalid input. Defaulting to 1 CPU core.")
        return 1

def main():
    # Step 1: Check for internet connection
    print_status("Checking for internet connection...", symbol="🌐")
    wait_for_internet()

    # Step 2: Install required packages
    print_status("Installing dependencies...", symbol="🛠️")
    install_requirements()

    # Step 3: Run configuration setup
    print_status("Running configuration setup...", symbol="🛠️")
    config_path = setup_config()

    # Step 4: Validate configuration
    print_status("Validating configuration...", symbol="✅")
    if not validate_config(config_path):
        print_status("Environment setup is incomplete. Please resolve the issues in the configuration file.", symbol="❌")
        return

    # Get the number of CPU cores to use from the user
    num_workers = get_user_core_input()

    # Create a pool of worker processes
    print(f"\n🚀 Starting {num_workers} worker(s)...\n")
    with Pool(processes=num_workers) as pool:
        pool.map(worker_process, range(num_workers))

if __name__ == "__main__":
    main()
