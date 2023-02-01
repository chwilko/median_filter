import numpy as np


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


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from tensorflow_addons.image import median_filter2d

    shape = (5, 5, 3)
    src = Source(shape)
    frame = src.get_data()
    frame2 = median_filter2d(frame, filter_shape=(3, 3))

    fig, axs = plt.subplots(3)
    for i in range(shape[-1]):
        axs[i].pcolor(frame[:, :, i])

    fig, axs = plt.subplots(3)
    for i in range(shape[-1]):
        axs[i].pcolor(frame2[:, :, i])

    plt.show()
