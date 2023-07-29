"""
Modulus responsible for sending logs to the console.
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(threadName)s] [%(levelname)s]: %(message)s",
)


def log(message: str):
    """Send log to console.
    Send log to console if self.verbose

    Args:
        message (str): log message
    """
    logging.info(message)
