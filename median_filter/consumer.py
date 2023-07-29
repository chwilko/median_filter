"""
Consumer is worker on single thread which takes data from one queue, and consume it.
According to the Producer-Consumer Paradigm.
"""
from multiprocessing import Queue
from threading import Thread
from typing import Any, Callable

from .common import StopValue


class Consumer(Thread):
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

    def __init__(
        self,
        queue: Queue,
        fun: Callable[[Any], Any],
        *,
        name: str = None,
        daemon: bool = None,
    ) -> None:
        """Initialize self.

        Args:
            queue (multiprocessing.Queue): queue with data to convert.
                Must be ended by median_filter.StopValue.
            fun (Callable[[Any], Any]): function to consume data from queue.
            name (str, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to None.
        """
        super().__init__(name=name, daemon=daemon)
        self.queue = queue
        self.fun = fun

    def run(self):
        """Method representing the thread's activity."""
        while 1:
            if self.queue.empty():
                continue
            data = self.queue.get()
            if isinstance(data, StopValue):
                self.queue.put(StopValue())
                break
            self.fun(data)
