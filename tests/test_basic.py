import random

import pytest

from median_filter import Queue, StopValue
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
    fun = lambda: 1
    prod = Producer(
        queue,
        fun,
        interval=0,
        n_steps=n,
    )
    prod.start()

    prod.join()
    for _ in range(n):
        assert queue.get() == fun()

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
    for el in values:
        queue_in.put(el)
    queue_in.put(StopValue())
    broker = Broker(
        queue_in=queue_in,
        queue_out=queue_out,
        fun=fun,
    )
    broker.start()

    broker.join()

    for el_in in values:
        el_out = queue_out.get()
        assert el_out == fun(el_in)

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
    for el in values:
        queue.put(el)
    queue.put(StopValue())
    consumer = Consumer(
        queue=queue,
        fun=fun1,
    )

    consumer.start()

    consumer.join()

    for i, el_in in enumerate(values):
        assert rets[i] == fun(el_in)

    last = queue.get()
    assert isinstance(last, StopValue)
    assert queue.empty()
