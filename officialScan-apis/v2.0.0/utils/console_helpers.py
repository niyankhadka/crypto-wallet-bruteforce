import os


def clear_console():
    """Clears the console output for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_status(message, symbol="✅"):
    """Prints a formatted status message with an optional symbol."""
    print(f"{symbol} {message}")


def print_separator():
    """Prints a visual separator for better console readability."""
    print("=" * 50)
