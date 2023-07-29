"""
Tests on module recorder which is responsible for saving images.
"""
import os
from shutil import rmtree

import numpy as np
import pytest
from skimage.io import imread

from median_filter import Queue
from median_filter.recorder import PictureRecorder, _Recorder

TIMEOUT = 0.1


def test_preparing_file():
    """Test valid create output folder."""
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)
    _Recorder(
        folder_name,
        file_name,
    )
    assert os.path.exists(folder_name)

    _Recorder(
        folder_name,
        file_name,
    )
    assert os.path.exists(folder_name)


@pytest.mark.parametrize("dim", (1, 3, 4))
def test_use_next_names(dim: int):
    """Test of setting the correct names of subsequent saved files.

    Args:
        dim (int): number of picture channels.
    """
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)
    rec = _Recorder(
        folder_name,
        file_name,
    )
    assert os.path.exists(folder_name)

    for _ in range(3):
        rec.save_to_file(np.random.random((3, 3, dim)))

    for i in range(3):
        assert f"{file_name}_{i}.png" in os.listdir(folder_name)


@pytest.mark.parametrize("dim", (1, 3, 4))
def test_save_pictures(dim: int):
    """Test of proper image storage.

    Args:
        dim (int): number of picture channels.
    """
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)
    rec = _Recorder(
        folder_name,
        file_name,
    )
    if dim == 1:
        pics = [np.random.random((5, 5)) for _ in range(5)]
    else:
        pics = [np.random.random((5, 5, dim)) for _ in range(5)]
    for pic in pics:
        rec.save_to_file(pic)

    for i, pic in enumerate(pics):
        saved_pic = imread(os.sep.join([folder_name, f"{file_name}_{i}.png"]))
        expected_pic = (255 * pic).astype(np.dtype("uint8"))
        assert (saved_pic == expected_pic).all()


@pytest.mark.parametrize("n_recorders", (1, 2, 6))
def test_save_pictures_n_recorders(n_recorders: int):
    """
    PictureRecorder standard operation test on n threads.
    """
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)

    # queue preparing
    queue: Queue = Queue()
    pics = [np.random.random((10, 10, 3)) for _ in range(300)]
    for pic in pics:
        queue.put(pic)
    # recorders preparing

    recorders = [
        PictureRecorder(
            queue,
            folder_name,
            file_name,
            timeout=TIMEOUT,
        )
    ]
    for _ in range(n_recorders):
        recorders.append(
            PictureRecorder(
                queue,
                folder_name,
                file_name,
                previous_recorder=recorders[-1],
                timeout=TIMEOUT,
            )
        )

    for recorder in recorders:
        recorder.start()
    for recorder in recorders:
        recorder.join()

    for i, pic in enumerate(pics):
        saved_pic = imread(os.sep.join([folder_name, f"{file_name}_{i}.png"]))
        expected_pic = (255 * pic).astype(np.dtype("uint8"))
        assert (saved_pic == expected_pic).all()
