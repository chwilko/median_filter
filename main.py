import numpy as np

from median_filter import MedianFilter, PictureRecorder, Producer, Queue, set_n_steps


class Source:
    def __init__(self, source_shape: tuple):
        self._source_shape: tuple = source_shape

    def get_data(self) -> np.ndarray:
        rows, cols, channels = self._source_shape
        return np.random.randint(
            256,
            size=rows * cols * channels,
            dtype=np.uint8,
        ).reshape(self._source_shape)


def main():
    timeout = 2
    input_shape = (768, 1024, 3)
    new_frame_shape = (512, 384)
    filter_shape = (5, 5, 1)
    interval = 50 / 1000
    n_steps = 100
    counter = set_n_steps(n_steps)
    folder_name = "processed"
    file_name = "output"

    queue0: Queue = Queue()
    queue1: Queue = Queue()

    src = Source(input_shape)

    producer = Producer(
        queue0,
        lambda: (next(counter), src.get_data()),
        interval,
    )
    broker = MedianFilter(
        queue_in=queue0,
        queue_out=queue1,
        new_frame_shape=new_frame_shape,
        filter_shape=filter_shape,
        timeout=timeout,
    )
    consumer = PictureRecorder(
        queue1,
        folder_name,
        file_name,
        file_ext="png",
        timeout=timeout,
    )

    producer.start()
    consumer.start()
    broker.start()

    producer.join()
    broker.join()
    consumer.join()


if __name__ == "__main__":
    main()
