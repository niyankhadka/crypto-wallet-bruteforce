import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(name="crypto_wallet_scanner"):
    """
    Setup a logger with both file and console handlers.
    File logs rotate when they reach 5MB.
    
    :param name: Logger name
    :return: Configured logger instance
    """
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation (max 5MB per file, keep 5 backups)
    log_file = os.path.join(logs_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler (INFO level only)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Add handlers if not already present
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def log_wallet_found(logger, mnemonic, network, address, balance):
    """Log when a wallet with balance is found."""
    logger.warning(f"💰 WALLET FOUND - Network: {network}, Address: {address}, Balance: {balance}, Mnemonic: {mnemonic}")


def log_session_start(logger, config_path):
    """Log session start information."""
    logger.info(f"🚀 Session started with config: {config_path}")


def log_session_end(logger, total_checks, total_found, duration):
    """Log session end information."""
    logger.info(f"🛑 Session ended - Total checks: {total_checks}, Total wallets found: {total_found}, Duration: {duration}")
