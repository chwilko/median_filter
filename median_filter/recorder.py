"""
Recorder is special consumer which get picture from queue,
and save it.
"""
import os
from multiprocessing import Queue
from threading import Lock

import numpy as np
from skimage.io import imsave

from .consumer import Consumer


class _Recorder:
    """Class to record pictures"""

    def __init__(
        self,
        folder_name: str,
        file_name: str,
        file_ext: str = "png",
    ) -> None:
        """Initialize self.

        Args:
            folder_name (str): folder to save pictures
            file_name (str): name pattern to save pictures.
            file_ext (str, optional): Extension for file to record. Defaults to "png".
        """
        self.folder_name = folder_name
        self.file_name = file_name
        self.file_ext = file_ext
        self._i = 0
        self.lock = Lock()
        self.make_folder()

    def make_folder(self) -> None:
        """method prepare folder to save pictures."""
        with self.lock:
            if not os.path.exists(self.folder_name):
                os.mkdir(self.folder_name)

    def _new_name(self) -> str:
        """method get new unique name to save file.

        Returns:
            str: unique name
        """
        with self.lock:
            name = os.sep.join(
                [self.folder_name, f"{self.file_name}_{self._i}.{self.file_ext}"]
            )
            self._i += 1
        return name

    def save_to_file(self, frame: np.ndarray) -> None:
        """save frame to file.

        Args:
            frame (np.ndarray): frame representing the picture
        """
        name = self._new_name()
        if frame.shape[-1] == 1:
            frame = frame[:, :, 0]
        imsave(
            name,
            arr=(255 * frame).astype(np.dtype("uint8")),
        )


class PictureRecorder(Consumer):
    """
    Takes picture data from queue and save them as picture in set folder.
    Parameter previous_recorder = consumer0 let save pictures on some threads and save order
    example use:

        folder_name = "folder_name"
        file_name = "file_name"

        queue1: Queue = Queue()

        consumer0 = PictureRecorder(queue1, folder_name, file_name)
        consumer1 = PictureRecorder(queue1, folder_name, file_name, previous_recorder = consumer0)

        consumer0.start()
        consumer1.start()
        consumer0.join()
        consumer1.join()
    """

    COUNTER = 0

    def __init__(
        self,
        queue: Queue,
        folder_name: str,
        file_name: str,
        file_ext: str = "png",
        *,
        previous_recorder=None,
        name=None,
        daemon=None,
        verbose: bool = True,
    ) -> None:
        """
        Args:
            queue (Queue): queue with picture data ended by StopValue
            folder_name (str): folder to save pictures
            file_name (str): name pattern to save pictures.
            file_ext (str, optional): Extension for file to record. Defaults to "png".
            previous_recorder (PictureRecorder, optional): Prievious PictureRecorder.
                this case let save pictures on some threads and save order. Defaults to None.
            daemon (bool, optional): description below. Defaults to False.
            verbose (bool, optional): If True thread loged. Defaults to True.
        """
        if previous_recorder is None:
            self._rec = _Recorder(folder_name, file_name, file_ext=file_ext)
        else:
            self._rec = previous_recorder._rec
        if name is None:
            name = f"PictureRecorder-{PictureRecorder.COUNTER}"
        PictureRecorder.COUNTER += 1

        super().__init__(
            queue,
            self._rec.save_to_file,
            name=name,
            daemon=daemon,
            verbose=verbose,
        )
