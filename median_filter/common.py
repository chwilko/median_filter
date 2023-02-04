class StopValue:
    """
    Stop token to use in multiprocessing.
    Queue to say information that queue has not and will not have any more values.
    """

    def __init__(self) -> None:
        pass


def set_n_steps(n: int):
    """This iterator yield n times True. Yields False next times.

    Args:
        n (int): This iterator yield n times True. Yields False next times.

    Yields:
        bool: n times True. False next times
    """
    i = 0
    while 1:
        yield i < n
        i += 1
