"""
Tests on modules producer, broker and consumer
which realizing extended consumer-producer paradigm.
"""
import random
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

# def test_porducer_error_in_producing():
#     """Producer catching errors.
#     """
#     n_steps= 100
#     queue: Queue = Queue()
#     counter = set_n_steps(n_steps)
#     fun = lambda: (next(counter), 1 / random.randint(-1, 1))  # noqa
#     prod = Producer(
#         queue,
#         fun,
#         interval=0,
#     )
#     prod.start()

#     prod.join()
#     # probability for raise assert error in working code is (1/3)**100. IMO acceptable.
#     assert not queue.empty()


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
