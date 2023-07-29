"""
Common objects for other project files.
"""


class StopValue:
    """
    Stop token to use in multiprocessing.
    Queue to say information that queue has not and will not have any more values.
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Stop Value Token"

    def __repr__(self) -> str:
        return "Stop Value Token"


def set_n_steps(n_steps: int):
    """This iterator yield n_steps times True. Yields False next times.

    Args:
        n_steps (int): This iterator yield n_steps times True. Yields False next times.

    Yields:
        bool: n_steps times True. False next times
    """
    i = 0
    while 1:
        yield i < n_steps
        i += 1
