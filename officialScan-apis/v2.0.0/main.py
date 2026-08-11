import time
import asyncio
from datetime import datetime, timedelta
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
    print_separator,
    setup_logger,
    log_wallet_found,
    log_session_start,
    log_session_end
)

logger = setup_logger()


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
        logger.error("Configuration validation failed. Setup incomplete.")
        return
    
    log_session_start(logger, config_path)

    # Start the continuous checking loop
    checked_counter = 1
    script_start_time = time.time()
    last_check_duration = timedelta(0)
    last_api_check_duration = timedelta(0)
    last_balance_status = "No balance found"
    total_balances_found = 0

    print("\n🔁 Starting continuous wallet generation and balance checks... (Press Ctrl+C to stop)\n")

    try:
        while True:
            # Clear console before starting a new check
            clear_console()

            check_start_time = time.time()
            total_elapsed_time = timedelta(seconds=(check_start_time - script_start_time))

            # Display script runtime, last check info, API check time, and balance status at the top
            print_separator()
            print_status(f"Total Script Runtime: {total_elapsed_time}", symbol="⏱️")
            print_status(f"Checked {checked_counter} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", symbol="🔄")
            
            if checked_counter > 1:
                print_status(f"Previous Check {checked_counter - 1} completed in {last_check_duration}", symbol="✅")
                print_status(f"Previous API Check Time: {last_api_check_duration}", symbol="🌐")
                print_status(f"Previous Check Result: {last_balance_status}", symbol="💰")
                print_status(f"Total Balances Found So Far: {total_balances_found}", symbol="📊")
            print_separator()

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

            # Step 10: Check balances and save if found (with retry logic)
            api_start_time = time.time()
            max_retries = 3
            retry_count = 0
            balances_found = False
            
            while retry_count < max_retries:
                try:
                    balances_found = asyncio.run(run_checks(derived_addresses, mnemonic))
                    break  # Success, exit retry loop
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # Exponential backoff: 2, 4, 8 seconds
                        print(f"⚠️  API check failed (attempt {retry_count}/{max_retries}): {e}")
                        print(f"⏳ Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        print(f"❌ API check failed after {max_retries} attempts: {e}")
                        balances_found = False
            
            api_end_time = time.time()
            last_api_check_duration = timedelta(seconds=(api_end_time - api_start_time))

            # Update balance status and total count
            if balances_found:
                last_balance_status = "Balance Found!"
                total_balances_found += 1
                logger.warning(f"🎉 WALLET WITH BALANCE FOUND! Mnemonic: {mnemonic}")
            else:
                last_balance_status = "No balance found"

            # Track overall check timing
            check_end_time = time.time()
            last_check_duration = timedelta(seconds=(check_end_time - check_start_time))

            # Increment checked counter for the next iteration
            checked_counter += 1

    except KeyboardInterrupt:
        print_status("Script manually stopped by user.", symbol="🛑")
        total_run_time = timedelta(seconds=(time.time() - script_start_time))
        print_status(f"Total script runtime: {total_run_time}", symbol="⏱️")
        print_status(f"Total balances found during the session: {total_balances_found}", symbol="📊")
        log_session_end(logger, checked_counter - 1, total_balances_found, total_run_time)


if __name__ == "__main__":
    main()