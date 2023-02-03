import numpy as np

from median_filter import MedianFilter, PictureRecorder, Producer, Queue


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
    input_shape = (1024, 768, 3)
    new_frame_shape = (512, 384)
    filter_shape = (5, 5, 1)
    interval = 50 / 1000
    n_steps = 100
    folder_name = "processed"
    file_name = "output"

    queue0: Queue = Queue()
    queue1: Queue = Queue()

    src = Source(input_shape)

    producer = Producer(queue0, src.get_data, interval, n_steps)
    broker = MedianFilter(
        queue_in=queue0,
        queue_out=queue1,
        new_frame_shape=new_frame_shape,
        filter_shape=filter_shape,
    )
    consumer = PictureRecorder(queue1, folder_name, file_name, file_ext="png")

    producer.start()
    consumer.start()
    broker.start()

    producer.join()
    broker.join()
    consumer.join()


if __name__ == "__main__":
    main()
