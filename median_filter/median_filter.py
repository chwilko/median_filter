from multiprocessing import Queue
from typing import Tuple

import numpy as np
from skimage.filters import median
from skimage.transform import resize

from .basic import Broker


def _resize_median_filter(
    frame: np.ndarray,
    new_frame_shape: Tuple[int, int],
    footprint: np.ndarray,
) -> np.ndarray:
    """Function resize frame using skimage.transform.resize and
        use on frame skimage.filters.median.

    Args:
        frame (np.ndarray): frame to convert
        new_frame_shape (Tuple[int, int]): new shape after resize
        footprint (np.ndarray): matrix of 0 and 1 indicating values to median

    Returns:
        np.ndarray: frame after resize and median filter
    """
    frame = resize(frame, new_frame_shape)
    frame = median(frame, footprint=footprint)
    return frame


class MedianFilter(Broker):
    """
    Takes data from one queue, converts it, and puts it into another as distinct thread.
    example use:

    new_frame_shape = (512, 384)
    filter_shape = (5, 5, 1)

    queue0: Queue = Queue()
    queue1: Queue = Queue()

    broker = MedianFilter(
        queue_in=queue0,
        queue_out=queue1,
        new_frame_shape=new_frame_shape,
        filter_shape=filter_shape,
    )

    broker.start()
    broker.join()
    """

    def __init__(
        self,
        queue_in: Queue,
        queue_out: Queue,
        new_frame_shape: Tuple[int, int],
        filter_shape: Tuple[int, int, int],
        *,
        name: str = None,
        daemon: bool = False,
    ) -> None:
        """
        Args:
            queue_in (multiprocessing.Queue): queue with data to convert ended by StopValue
            queue_out (multiprocessing.Queue): queue for converted data. Will be ended by StopValue
            new_frame_shape (Tuple[int, int]): final shape to reshape data from queue_in
            filter_shape (Tuple[int, int, int]): shape of the filter to be used by median filter
            name (_type_, optional): the thread name. By default, a unique name is constructed of
                the form "Thread-N" where N is a small decimal number.
            daemon (bool, optional): description below. Defaults to False.

        """
        super().__init__(
            queue_in,
            queue_out,
            lambda frame: _resize_median_filter(
                frame,
                new_frame_shape=new_frame_shape,
                footprint=np.ones(filter_shape),
            ),
            name=name,
            daemon=daemon,
        )
