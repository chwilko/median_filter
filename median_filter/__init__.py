"""
Package implements Producer - Consumer design pattern with a small extension.
This extension is Broker.

Producer produces data for the queue;
Consumer consumes data from the queue;
Broker uses data from the first queue to add to the second queue.

Moreover, package implements a special case of Broker (MedianFilter)
nad a special case of Consumer (Recorder).
"""
from multiprocessing import Queue

from .broker import Broker
from .common import set_n_steps
from .consumer import Consumer
from .median_filter import MedianFilter
from .producer import Producer
from .recorder import PictureRecorder
from .worker import Worker

__all__ = [
    "Broker",
    "Consumer",
    "Queue",
    "MedianFilter",
    "PictureRecorder",
    "Producer",
    "Worker",
    "set_n_steps",
]
