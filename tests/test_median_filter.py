from typing import Tuple

import numpy as np
import pytest

from median_filter import Queue, StopValue
from median_filter.median_filter import MedianFilter, _resize_median_filter

median_check_params = (
    ((3, 3), (2**4, 2**10)),
    ((5, 5), (2**4, 2**3)),
    ((3, 7), (2**8, 2**8)),
    ((9, 1), (2**7, 2**6)),
)


def median(values: np.ndarray):
    values = sorted(values.flatten())
    n = len(values)
    if n % 2:
        return values[len(values) // 2]
    else:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2


def random_median_check(
    values0: np.ndarray,
    values1: np.ndarray,
    shape: Tuple[int, int],
    pic_shape: Tuple[int, int],
):
    mv = [i // 2 for i in shape]
    for _ in range(30):
        pos = (
            np.random.randint(mv[0], pic_shape[0] - mv[0] - 1),
            np.random.randint(mv[1], pic_shape[1] - mv[1] - 1),
            np.random.randint(0, 3),
        )
        tmp_array = values0[
            pos[0] - mv[0] : pos[0] + mv[0] + 1,
            pos[1] - mv[1] : pos[1] + mv[1] + 1,
            pos[2],
        ]
        expected_median = median(tmp_array)
        if not values1[pos[0], pos[1], pos[2]] == expected_median:
            return False
    return True


def test_resize_median_filter_shape():
    pics = [np.random.random((128, 512, 3)) for _ in range(10)]

    for pic in pics:
        new_pic = _resize_median_filter(
            pic,
            (64, 256),
            np.ones((2, 2, 1)),
        )
        assert new_pic.shape == (64, 256, 3)


@pytest.mark.parametrize("median_shape, pic_shape", median_check_params)
def test_resize_median_filter_median(median_shape, pic_shape):
    pic_shape = (128, 512)
    pics = [np.random.random((*pic_shape, 3)) for _ in range(3)]
    for pic in pics:
        new_pic = _resize_median_filter(
            pic,
            pic_shape,
            np.ones((*median_shape, 1)),
        )

        assert random_median_check(pic, new_pic, median_shape, pic_shape)


@pytest.mark.parametrize("median_shape, pic_shape", median_check_params)
def test_MedianFilter(median_shape, pic_shape):
    pic_shape = (128, 256)
    queue_in = Queue()
    queue_out = Queue()

    pics = [np.random.random((*pic_shape, 3)) for _ in range(3)]

    for pic in pics:
        queue_in.put(pic)
    queue_in.put(StopValue())

    working_thread = MedianFilter(
        queue_in,
        queue_out,
        pic_shape,
        (*median_shape, 1),
    )

    working_thread.start()

    working_thread.join()

    for pic in pics:
        new_pic = queue_out.get()
        assert random_median_check(pic, new_pic, median_shape, pic_shape)

    assert isinstance(queue_out.get(), StopValue)
