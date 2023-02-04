import random

import pytest

from median_filter import Queue, StopValue, set_n_steps
from median_filter.basic import Broker, Consumer, Producer


@pytest.mark.parametrize(
    "n",
    (
        2,
        100,
        30,
    ),
)
def test_porducer(n):
    queue: Queue = Queue()
    counter = set_n_steps(n)
    fun = lambda: (next(counter), 1)
    prod = Producer(
        queue,
        fun,
        interval=0,
    )
    prod.start()

    prod.join()
    for _ in range(n):
        assert queue.get() == fun()[1]

    last = queue.get()
    assert isinstance(last, StopValue)
    assert queue.empty()


@pytest.mark.parametrize(
    "fun, values",
    (
        (lambda x: 2 * x, list(range(4))),
        (
            lambda x: sum(x),
            [[random.random() for _ in range(random.randint(2, 10))] for _ in range(4)],
        ),
    ),
)
def test_broker(fun, values):
    queue_in: Queue = Queue()
    queue_out: Queue = Queue()
    for val in values:
        queue_in.put(val)
    queue_in.put(StopValue())
    broker = Broker(
        queue_in=queue_in,
        queue_out=queue_out,
        fun=fun,
    )
    broker.start()

    broker.join()

    for val_in in values:
        val_out = queue_out.get()
        assert val_out == fun(val_in)

    last = queue_out.get()
    assert isinstance(last, StopValue)
    assert queue_out.empty()

    last2 = queue_in.get()
    assert isinstance(last2, StopValue)
    assert queue_in.empty()


@pytest.mark.parametrize(
    "fun, values",
    (
        (lambda x: 2 * x, list(range(4))),
        (
            lambda x: sum(x),
            [[random.random() for _ in range(random.randint(2, 10))] for _ in range(4)],
        ),
    ),
)
def test_consumer(fun, values):
    rets = []
    fun1 = lambda x: rets.append(fun(x))
    queue: Queue = Queue()
    for val in values:
        queue.put(val)
    queue.put(StopValue())
    consumer = Consumer(
        queue=queue,
        fun=fun1,
    )

    consumer.start()

    consumer.join()

    for i, val_in in enumerate(values):
        assert rets[i] == fun(val_in)

    last = queue.get()
    assert isinstance(last, StopValue)
    assert queue.empty()
