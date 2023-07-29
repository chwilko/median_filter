"""
Consumer is worker on single thread which takes data from one queue, and consume it.
According to the Producer-Consumer Paradigm.
"""
from multiprocessing import Queue
from queue import Empty
from typing import Any, Callable

from .worker import Worker


class Consumer(Worker):
    """
    Takes data from queue and use them as distinct thread.

    Usage example:
        queue0: Queue = Queue()
        queue1: Queue = Queue()

        producer = Producer(queue0, producer_foo, interval)
        broker = Broker(queue0, queue1, broker_foo)
        consumer = Consumer(queue1, consumer_foo)

        producer.start()
        broker.start()
        consumer.start()

        producer.join()
        broker.join()
        consumer.join()
    """

    COUNTER = 0

    def __init__(
        self,
        queue: Queue,
        fun: Callable[[Any], Any],
        *,
        name: str = None,
        daemon: bool = None,
        verbose: bool = True,
        timeout: float = 10.0,
    ) -> None:
        """Initialize self.

        Args:
            queue (multiprocessing.Queue): queue with data to convert.
            fun (Callable[[Any], Any]): function to consume data from queue.
            name (str, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to None.
            verbose (bool, optional): If True thread loged. Defaults to True.
            timeout (float, optional): Timeout for queue get. Defaults to 5.0.
        """
        if name is None:
            name = f"Consumer-{Consumer.COUNTER}"
        Consumer.COUNTER += 1

        super().__init__(name=name, daemon=daemon, verbose=verbose)
        self.queue = queue
        self.fun = fun
        self.timeout = timeout

    def run(self):
        """Method representing the thread's activity."""
        while 1:
            try:
                data = self.queue.get(timeout=self.timeout)
            except Empty:
                return
            try:
                self.fun(data)
            except Exception as error:  # pylint: disable = broad-exception-caught
                self.warning(str(error))

            self.log("Consumed.")
