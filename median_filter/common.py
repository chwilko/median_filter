"""
Common objects for other project files.
"""


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
