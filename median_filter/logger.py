import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(threadName)s] [%(levelname)s]: %(message)s",
)


def log(message: str):
    logging.info(message)
