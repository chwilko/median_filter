from multiprocessing import Queue
from typing import Tuple

import numpy as np
from skimage.filters import median as median_filter
from skimage.transform import resize

from .basic import Broker


def _resize_median_filter(
    frame: np.ndarray,
    new_frame_shape: Tuple[int, int],
    footprint: np.ndarray,
) -> np.ndarray:
    frame = resize(frame, new_frame_shape)
    frame = median_filter(frame, footprint=footprint)
    return frame


class MedianFilter(Broker):
    def __init__(
        self,
        queue_in: Queue,
        queue_out: Queue,
        new_frame_shape: Tuple[int, int],
        filter_shape: Tuple[int, int, int],
        **kwargs,
    ) -> None:
        super().__init__(
            queue_in,
            queue_out,
            lambda frame: _resize_median_filter(
                frame,
                new_frame_shape=new_frame_shape,
                footprint=np.ones(filter_shape),
            ),
            **kwargs,
        )
