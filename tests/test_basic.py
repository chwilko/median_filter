"""
Tests on modules producer, broker and consumer
which realizing extended consumer-producer paradigm.
"""
import random
from typing import Any, Callable, Iterable

import pytest

from median_filter import Broker, Consumer, Producer, Queue, StopValue, set_n_steps


@pytest.mark.parametrize(
    "n_steps",
    (
        2,
        100,
        30,
    ),
)
def test_porducer(n_steps: int):
    """Producer standard operation test.

    Args:
        n_steps (int): producer send n_steps data to queue.
    """
    queue: Queue = Queue()
    counter = set_n_steps(n_steps)
    fun = lambda: (next(counter), 1)  # noqa
    prod = Producer(
        queue,
        fun,
        interval=0,
    )
    prod.start()

    prod.join()
    for _ in range(n_steps):
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
def test_broker(fun: Callable, values: Iterable[Any]):
    """Broker standard operation test.

    Args:
        fun (Callable): function which transform values
        values (Iterable[Any]): list of values in one type
    """
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
def test_consumer(fun: Callable, values: Iterable[Any]):
    """Cnosumer standard operation test.

    Args:
        fun (Callable): function which transform values
        values (Iterable[Any]): list of values in one type
    """
    rets = []
    queue: Queue = Queue()
    for val in values:
        queue.put(val)
    queue.put(StopValue())
    consumer = Consumer(
        queue=queue,
        fun=lambda x: rets.append(fun(x)),
    )

    consumer.start()

    consumer.join()

    for i, val_in in enumerate(values):
        assert rets[i] == fun(val_in)

    last = queue.get()
    assert isinstance(last, StopValue)
    assert queue.empty()
