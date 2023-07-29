"""
Worker is abstract class for producer, broker and consumer.
"""
import logging
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(threadName)s] [%(levelname)s]: %(message)s",
)


class Worker(Thread):
    """
    Abstract class for producer, broker and consumer.
    Include common methods.
    """

    COUNTER = 0

    def __init__(
        self,
        *,
        name: str = None,
        daemon: bool = None,
        verbose: bool = True,
    ) -> None:
        """Initialize self.

        Args:
            queue (multiprocessing.Queue): queue for converted data.
            fun (Callable[[], Tuple[bool, Any]]): function to produce data.
                Data are producing while fun return (True, ...).
            interval (float, optional): interval to next function calling. Defaults to 0.
            name (str, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to None.
            verbose (bool, optional): If True thread loged. Defaults to True.
        """
        if name is None:
            name = f"Worker-{Worker.COUNTER}"
        Worker.COUNTER += 1

        super().__init__(name=name, daemon=daemon)
        self.verbose = verbose
        self.log("created")

    def __del__(self):
        self.log("closed")

    def log(self, message: str) -> None:
        """Send info log to console.
        Send log to console if self.verbose

        Args:
            message (str): log message
        """
        if self.verbose:
            logging.info(message)

    def warning(self, message: str) -> None:
        """Send warning log to console.
        Send log to console if self.verbose

        Args:
            message (str): log message
        """
        if self.verbose:
            logging.error(message)
