"""
Broker is worker on single thread which takes data from one queue,
converts it, and puts it into another as distinct thread.
"""
from multiprocessing import Queue
from threading import Thread
from typing import Any, Callable

from .common import StopValue


class Broker(Thread):
    """
    Takes data from one queue, converts it,
        and puts it into another as distinct thread.

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
        queue_in: Queue,
        queue_out: Queue,
        fun: Callable[[Any], Any],
        *,
        name: str = None,
        daemon: bool = None,
    ) -> None:
        """Initialize self.

        Args:
            queue_in (multiprocessing.Queue): queue with data to convert.
                Must be ended by median_filter.StopValue.
            queue_out (multiprocessing.Queue): queue for converted data.
            fun (Callable[[Any], Any]): function for data processing
            name (str, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to None.
        """
        super().__init__(name=name, daemon=daemon)
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.fun = fun

    def run(
        self,
    ):
        """Method representing the thread's activity."""
        while 1:
            if self.queue_in.empty():
                continue
            data = self.queue_in.get()
            if isinstance(data, StopValue):
                self.queue_in.put(StopValue())
                self.queue_out.put(StopValue())
                break
            self.queue_out.put(self.fun(data))
