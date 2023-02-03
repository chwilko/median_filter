import os
from shutil import rmtree

import numpy as np
import pytest
from skimage.io import imread

from median_filter import Queue, StopValue
from median_filter.recorder import PictureRecorder, _Recorder


def test_preparing_file():
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)
    rec = _Recorder(
        folder_name,
        file_name,
    )
    assert os.path.exists(folder_name)

    rec = _Recorder(
        folder_name,
        file_name,
    )
    assert os.path.exists(folder_name)


@pytest.mark.parametrize(
    "dim",
    (
        1,
        3,
        4,
    ),
)
def test_use_next_names(dim):
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


@pytest.mark.parametrize(
    "dim",
    (
        1,
        3,
        4,
    ),
)
def test_save_pictures(dim):
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


def test_save_pictures():
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)

    queue = Queue()
    pics = [np.random.random((10, 10, 3)) for _ in range(5)]

    for pic in pics:
        queue.put(pic)
    queue.put(StopValue())
    recorder = PictureRecorder(
        queue,
        folder_name,
        file_name,
    )

    recorder.start()
    recorder.join()

    for i, pic in enumerate(pics):
        saved_pic = imread(os.sep.join([folder_name, f"{file_name}_{i}.png"]))
        expected_pic = (255 * pic).astype(np.dtype("uint8"))
        assert (saved_pic == expected_pic).all()


def test_save_pictures_two_recorders():
    folder_name = os.sep.join(["tests", "try"])
    file_name = "test"
    if os.path.exists(folder_name):
        rmtree(folder_name)

    queue = Queue()
    pics = [np.random.random((10, 10, 3)) for _ in range(100)]

    for pic in pics:
        queue.put(pic)
    queue.put(StopValue())
    recorder = PictureRecorder(
        queue,
        folder_name,
        file_name,
    )
    recorder1 = PictureRecorder(
        queue,
        folder_name,
        file_name,
        previous_recorder=recorder,
    )

    recorder.start()
    recorder1.start()

    recorder.join()
    recorder1.join()

    for i, pic in enumerate(pics):
        saved_pic = imread(os.sep.join([folder_name, f"{file_name}_{i}.png"]))
        expected_pic = (255 * pic).astype(np.dtype("uint8"))
        assert (saved_pic == expected_pic).all()
