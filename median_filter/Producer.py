from time import sleep
from  multiprocessing import Queue, Process, Event

class Producer:
    def __init__(self, fun, *, args=[]):
        self.fun = lambda : fun(*args)

    def run(self, queue: Queue, interval: float, event: Event, steps: int=-1):
        while steps != 0:
            data = self.fun()
            queue.put(data)
            sleep(interval)
            steps -= 1
        event.set()


class Consumer:
    def __init__(self, fun, *, args=[]):
        self.fun = lambda x: fun(x, *args)

    def run(
        self,
        queue_in: Queue,
        queue_out: Queue,
        event: Event
    ):
        i = 0
        while not event.is_set() or not queue0.empty():
            if queue0.empty():
                continue
            # print(i, event.is_set(), queue0.empty())
            # i+=1
            data = queue_in.get()
            queue_out.put(self.fun(data))


if __name__ =="__main__":
    import random
    queue0 = Queue()
    queue1 = Queue()
    prod = Producer(lambda x, y: random.random() * (y-x) + x, args=[0,3])
    cons = Consumer(lambda x: 2 * x - 3)
    event = Event()
    proc = [
        Process(
            target=prod.run,
            args=(queue0, 1/1000, event, 100),
        ),
        Process(
            target=cons.run,
            args=(queue0, queue1, event),
        ),
    ]

    for p in proc:
        p.start()

    sleep(1)
    while not queue1.empty() or not queue0.empty():
        print(queue1.get())
