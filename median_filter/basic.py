from multiprocessing import Queue
from threading import Thread
from time import sleep

from .common import StopValue


class Producer(Thread):
    """
    Takes data and puts it into queue as distinct thread.

    example use:
        queue0: Queue = Queue()
        queue1: Queue = Queue()

        producer = Producer(queue0, producer_foo, interval, steps)
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
        fun,
        interval: float = 0,
        steps: int = -1,
        *,
        name: str = None,
        daemon: bool = False,
    ) -> None:
        """_summary_

        Args:
            queue (multiprocessing.Queue): queue for converted data. Will be ended by StopValue
            fun (_type_): _description_
            interval (float, optional): _description_. Defaults to 0.
            steps (int, optional): _description_. Defaults to -1.
            name (_type_, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to False.
        """
        super().__init__(name=name, daemon=daemon)
        self.queue = queue
        self.interval = interval
        self.steps = steps
        self.fun = fun

    def run(self):
        """Method representing the thread's activity."""
        while self.steps != 0:
            data = self.fun()
            self.queue.put(data)
            sleep(self.interval)
            self.steps -= 1
        self.queue.put(StopValue())


class Broker(Thread):
    """
    Takes data from one queue, converts it,
        and puts it into another as distinct thread.

    example use:
        queue0: Queue = Queue()
        queue1: Queue = Queue()

        producer = Producer(queue0, producer_foo, interval, steps)
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
        fun,
        *,
        name: str = None,
        daemon: bool = False,
    ) -> None:
        """_summary_

        Args:
            queue_in (multiprocessing.Queue): queue with data to convert ended by StopValue
            queue_out (multiprocessing.Queue): queue for converted data. Will be ended by StopValue
            fun (_type_): _description_
            name (_type_, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to False.
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


class Consumer(Thread):
    """
    Takes data from queue and use them as distinct thread.

    example use:
        queue0: Queue = Queue()
        queue1: Queue = Queue()

        producer = Producer(queue0, producer_foo, interval, steps)
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
        fun,
        *,
        name: str = None,
        daemon: bool = False,
    ) -> None:
        """_summary_

        Args:
            queue (multiprocessing.Queue): queue with data to convert ended by StopValue.
            fun (_type_): _description_
            name (_type_, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to False.
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
