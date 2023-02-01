from multiprocessing import Queue
import random
from threading import Thread
from time import sleep

# from queue import Queue


STOP_VALUE = "STOP_VALUE"


class Producer(Thread):
    def __init__(
        self,
        queue: Queue,
        interval: float,
        steps: int = -1,
        fun=lambda: random.random() * 3,
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
        self.queue.put(STOP_VALUE)


class Consumer(Thread):
    def __init__(
        self,
        queue_in: Queue,
        queue_out: Queue,
        fun=lambda x: 2 * x - 3,
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
            if data == STOP_VALUE:
                break
            self.queue_out.put(self.fun(data))


if __name__ == "__main__":
    import random

    queue0 = Queue()
    queue1 = Queue()
    prod = Producer(queue0, 10 / 1000, 100)
    cons = Consumer(queue0, queue1)

    prod.start()
    cons.start()

    prod.join()
    cons.join()

    while not queue1.empty() or not queue0.empty():
        print(queue1.get())
