from multiprocessing import Queue
from threading import Thread
from time import sleep

from .common import StopValue


class Producer(Thread):
    def __init__(
        self,
        queue: Queue,
        fun,
        interval: float = 0,
        steps: int = -1,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.queue = queue
        self.interval = interval
        self.steps = steps
        self.fun = fun

    def run(self):
        while self.steps != 0:
            data = self.fun()
            self.queue.put(data)
            sleep(self.interval)
            self.steps -= 1
        self.queue.put(StopValue())


class Broker(Thread):
    def __init__(
        self,
        queue_in: Queue,
        queue_out: Queue,
        fun,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.fun = fun

    def run(
        self,
    ):
        while 1:
            if self.queue_in.empty():
                continue
            data = self.queue_in.get()
            # if type(data) is StopValue:
            if isinstance(data, StopValue):
                self.queue_in.put(StopValue())
                self.queue_out.put(StopValue())
                break
            self.queue_out.put(self.fun(data))


class Consumer(Thread):
    def __init__(
        self,
        queue: Queue,
        fun,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.queue = queue
        self.fun = fun

    def run(self):
        while 1:
            if self.queue.empty():
                continue
            data = self.queue.get()
            # if type(data) is StopValue:
            if isinstance(data, StopValue):
                self.queue.put(StopValue())
                break
            self.fun(data)
