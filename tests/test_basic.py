"""
Tests on modules producer, broker and consumer
which realizing extended consumer-producer paradigm.
"""
import random
from time import sleep
from typing import Any, Callable, Iterable

import pytest

from median_filter import Broker, Consumer, Producer, Queue, set_n_steps

TIMEOUT = 0.1


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

    assert queue.empty()


def test_porducer_names():
    """Producer catching errors."""
    Producer.COUNTER = 0
    n_steps = 100
    queue: Queue = Queue()
    counter = set_n_steps(n_steps)
    fun = lambda: (next(counter), 1 / random.randint(-1, 1))  # noqa
    prod0 = Producer(
        queue,
        fun,
        interval=0.001,
    )
    prod1 = Producer(
        queue,
        fun,
        interval=0.001,
    )
    assert prod0.name == "Producer-0"
    assert prod1.name == "Producer-1"


def test_porducer_error_in_producing():
    """Producer catching errors."""
    n_steps = 100
    queue: Queue = Queue()
    counter = set_n_steps(n_steps)
    fun = lambda: (next(counter), 1 / random.randint(-1, 1))  # noqa
    prod = Producer(
        queue,
        fun,
        interval=0.001,
    )
    prod.start()

    prod.join()
    # probability for raise assert error in working code is (1/3)**100. IMO acceptable.
    assert not queue.empty()


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
def test_broker(fun: Callable[[Any], Any], values: Iterable[Any]):
    """Broker standard operation test.

    Args:
        fun (Callable[[Any], Any]): function which transform values
        values (Iterable[Any]): list of values in one type
    """
    queue_in: Queue = Queue()
    queue_out: Queue = Queue()
    for val in values:
        queue_in.put(val)
    broker = Broker(
        queue_in=queue_in,
        queue_out=queue_out,
        fun=fun,
        timeout=TIMEOUT,
    )
    broker.start()
    broker.join()

    for val_in in values:
        val_out = queue_out.get()
        assert val_out == fun(val_in)

    assert queue_out.empty()
    assert queue_in.empty()


def test_broker_error_in_transformation():
    """Broker error in transformation."""
    fun = lambda x: 2 / x  # noqa
    values = list(range(-2, 4))
    queue_in: Queue = Queue()
    queue_out: Queue = Queue()
    for val in values:
        queue_in.put(val)
    broker = Broker(
        queue_in=queue_in,
        queue_out=queue_out,
        fun=fun,
        timeout=TIMEOUT,
    )
    broker.start()
    broker.join()

    for val_in in values:
        if val_in == 0:
            continue
        val_out = queue_out.get()
        assert val_out == fun(val_in)

    assert queue_out.empty()
    assert queue_in.empty()


def test_broker_names():
    """Broker error in transformation."""
    Broker.COUNTER = 0
    values = list(range(-2, 4))
    queue_in: Queue = Queue()
    queue_out: Queue = Queue()
    for val in values:
        queue_in.put(val)
    broker0 = Broker(
        queue_in=queue_in,
        queue_out=queue_out,
        fun=lambda x: x,
        timeout=TIMEOUT,
    )
    broker1 = Broker(
        queue_in=queue_in,
        queue_out=queue_out,
        fun=lambda x: x,
        timeout=TIMEOUT,
    )
    assert broker0.name == "Broker-0"
    assert broker1.name == "Broker-1"


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
    """Consumer standard operation test.

    Args:
        fun (Callable): function which transform values
        values (Iterable[Any]): list of values in one type
    """
    rets = []
    queue: Queue = Queue()
    for val in values:
        queue.put(val)

    consumer = Consumer(
        queue=queue,
        fun=lambda x: rets.append(fun(x)),
        timeout=TIMEOUT,
    )

    consumer.start()

    consumer.join()

    for i, val_in in enumerate(values):
        assert rets[i] == fun(val_in)

    assert queue.empty()


def test_consumer_error_in_consume():
    """Consumer error in consume."""
    fun = lambda x: 2 / x  # noqa
    values = list(range(-2, 4))
    rets = []
    queue: Queue = Queue()
    for val in values:
        queue.put(val)

    consumer = Consumer(
        queue=queue,
        fun=lambda x: rets.append(fun(x)),
        timeout=TIMEOUT,
    )

    consumer.start()

    consumer.join()
    move = 0
    for i, val_in in enumerate(values):
        if val_in == 0:
            move = 1
            continue
        assert rets[i - move] == fun(val_in)

    assert queue.empty()


def test_consumer_names():
    """Consumer error in consume."""
    Consumer.COUNTER = 0
    values = list(range(-2, 4))
    queue: Queue = Queue()
    for val in values:
        queue.put(val)

    consumer0 = Consumer(
        queue=queue,
        fun=lambda x: x,
        timeout=TIMEOUT,
    )

    consumer1 = Consumer(
        queue=queue,
        fun=lambda x: x,
        timeout=TIMEOUT,
    )
    queue.cancel_join_thread()
    sleep(0.1)
    assert consumer0.name == "Consumer-0"
    assert consumer1.name == "Consumer-1"
