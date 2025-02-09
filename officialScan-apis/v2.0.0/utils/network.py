import time
import socket
from datetime import datetime
from utils import clear_console


def wait_for_internet(timeout=5):
    """
    Waits until the internet connection is available.
    Repeatedly checks connection until successful, clearing the console and tracking attempts.

    :param timeout: Time to wait between retries (in seconds).
    """
    connection_attempts = 1  # Track the number of connection attempts

    while True:
        try:
            # Test connection to a well-known server (Google's public DNS server)
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            print("✅ Internet connection is available.")
            return True
        except (OSError, socket.timeout):
            clear_console()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"❌ No internet connection. Attempt {connection_attempts} at {current_time}. Retrying in {timeout} seconds...")
            connection_attempts += 1
            time.sleep(timeout)