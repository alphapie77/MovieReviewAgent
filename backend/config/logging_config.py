"""
Centralized Logging Configuration for Phase 3 Multi-Agent System
Tracks all agent actions, errors, and performance metrics
"""

import logging
import colorlog
from datetime import datetime
from pathlib import Path

# Create outputs/logs directory if not exists
LOGS_DIR = Path(__file__).parent.parent / "outputs" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Log file path with timestamp
LOG_FILE = LOGS_DIR / f"agent_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def setup_logger(name: str = "MultiAgentSystem", level: str = "INFO") -> logging.Logger:
    """
    Setup centralized logger with both file and console handlers
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File Handler - Detailed logs
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console Handler - Colored output
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s | %(cyan)s%(name)s%(reset)s | %(message)s',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logger()


if __name__ == "__main__":
    # Test logging
    logger.debug("Debug message - detailed information")
    logger.info("Info message - general information")
    logger.warning("Warning message - something unexpected")
    logger.error("Error message - something failed")
    logger.critical("Critical message - system failure")
    
    print(f"\n✅ Logs saved to: {LOG_FILE}")
