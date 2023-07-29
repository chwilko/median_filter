"""
Producer is worker on single thread which takes data from one queue, and consume it.
According to the Producer-Consumer Paradigm.
"""
from multiprocessing import Queue
from threading import Thread
from time import sleep
from typing import Any, Callable, Tuple

from .common import StopValue


class Producer(Thread):
    """
    Takes data and puts it into queue as a distinct thread.

    Usage example:
        counter = set_n_steps(n_steps)
        queue0: Queue = Queue()
        queue1: Queue = Queue()

        producer = Producer(queue0, lambda: (next(counter), producer_foo), interval)
        broker = Broker(queue0, queue1, broker_foo)
        consumer = Consumer(queue1, consumer_foo)

        producer.start()
        broker.start()
        consumer.start()

        producer.join()
        broker.join()
        consumer.join()

    """

    def __init__(
        self,
        queue: Queue,
        fun: Callable[[], Tuple[bool, Any]],
        interval: float = 0,
        *,
        name: str = None,
        daemon: bool = None,
    ) -> None:
        """Initialize self.

        Args:
            queue (multiprocessing.Queue): queue for converted data.
                Will be ended by median_filter.StopValue.
            fun (Callable[[], Tuple[bool, Any]]): function to produce data.
                Data are producing while fun return (True, ...).
            interval (float, optional): interval to next function calling. Defaults to 0.
            name (str, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to None.
        """
        super().__init__(name=name, daemon=daemon)
        self.queue = queue
        self.interval = interval
        self.fun = fun

    def run(self):
        """Method representing the thread's activity."""
        while 1:
            processing, data = self.fun()
            if not processing:
                break
            self.queue.put(data)
            sleep(self.interval)
        self.queue.put(StopValue())
