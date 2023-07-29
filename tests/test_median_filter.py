"""
Tests on module median_filter which is responsible for saving images.
"""
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


def median(values: np.ndarray) -> float:
    """Function return median of values.

    Args:
        values (np.ndarray): Array with values

    Returns:
        float: median of values
    """
    values_list = sorted(values.flatten())
    n_values = len(values_list)
    if n_values % 2:
        return values_list[len(values_list) // 2]
    return (
        values_list[len(values_list) // 2 - 1] + values_list[len(values_list) // 2]
    ) / 2


def random_median_check(
    values0: np.ndarray,
    values1: np.ndarray,
    median_shape: Tuple[int, int],
    pic_shape: Tuple[int, int],
    k_trials: int = 30,
) -> bool:
    """Function check randomly k_trials points in input array and output array.

    Args:
        values0 (np.ndarray): input array
        values1 (np.ndarray): output array
        median_shape (Tuple[int, int]): median filter shape.
        pic_shape (Tuple[int, int]): input picture (values0) shape
        k_trials (int, optional): Function apply k_trials random tests. Defaults to 30.

    Returns:
        bool: True if function did not find errors in output.
    """
    padding_shape = [i // 2 for i in median_shape]
    for _ in range(k_trials):
        pos = (
            np.random.randint(padding_shape[0], pic_shape[0] - padding_shape[0] - 1),
            np.random.randint(padding_shape[1], pic_shape[1] - padding_shape[1] - 1),
            np.random.randint(0, 3),
        )
        tmp_array = values0[
            pos[0] - padding_shape[0] : pos[0] + padding_shape[0] + 1,
            pos[1] - padding_shape[1] : pos[1] + padding_shape[1] + 1,
            pos[2],
        ]
        expected_median = median(tmp_array)
        if not values1[pos[0], pos[1], pos[2]] == expected_median:
            return False
    return True


def test_resize_median_filter_shape():
    """_resize_median_filter standard operation test resizing.

    Args:
        median_shape (Tuple[int, int]): shape of median filter
        pic_shape (Tuple[int, int]): shape of picture
    """
    pics = [np.random.random((128, 512, 3)) for _ in range(10)]

    for pic in pics:
        new_pic = _resize_median_filter(
            pic,
            (64, 256),
            np.ones((2, 2, 1)),
        )
        assert new_pic.shape == (64, 256, 3)


@pytest.mark.parametrize("median_shape, pic_shape", median_check_params)
def test_resize_median_filter_median(
    median_shape: Tuple[int, int],
    pic_shape: Tuple[int, int],
):
    """_resize_median_filter standard operation test without resizing.

    Args:
        median_shape (Tuple[int, int]): shape of median filter
        pic_shape (Tuple[int, int]): shape of picture
    """
    pics = [np.random.random((*pic_shape, 3)) for _ in range(3)]
    for pic in pics:
        new_pic = _resize_median_filter(
            pic,
            pic_shape,
            np.ones((*median_shape, 1)),
        )

        assert random_median_check(pic, new_pic, median_shape, pic_shape)


@pytest.mark.parametrize("median_shape, pic_shape", median_check_params)
def test_MedianFilter(  # pylint: disable=invalid-name
    median_shape: Tuple[int, int],
    pic_shape: Tuple[int, int],
):
    """MedianFilter standard operation test.

    Args:
        median_shape (Tuple[int, int]): shape of median filter
        pic_shape (Tuple[int, int]): shape of picture
    """
    queue_in: Queue = Queue()
    queue_out: Queue = Queue()

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
