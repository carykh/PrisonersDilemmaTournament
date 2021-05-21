import numpy


def strategy(history, memory):
    """
    Look at the window of the last up to 10 moves.
    Defect if they've defected more than half the time or if they cooperate very often.
    Cooperate otherwise.
    """
    WINDOW_SIZE = 10
    OPPORTUNISTIC_DEFECTION_THRESHOLD = 0.8  # if they cooperated this often, defect
    MIN_WINDOW_SIZE_FOR_OPPORTUNISTIC_DEFECTION = 10  # don't cheat too early
    PUNITIVE_DEFECTION_THRESHOLD = 0.5  # if they defected at least this much, defect

    num_rounds = history.shape[1]
    if num_rounds < 1:
        return 1, None

    window_start = max(0, num_rounds - WINDOW_SIZE)
    window_end = num_rounds

    their_recent_moves = history[1, window_start:window_end]
    their_recent_stats = dict(
        zip(*numpy.unique(their_recent_moves, return_counts=True))
    )
    actual_window_size = len(their_recent_moves)

    cooperation_rate = their_recent_stats.get(1, 0) / actual_window_size
    defection_rate = their_recent_stats.get(0, 0) / actual_window_size

    choice = 1
    if (
        cooperation_rate >= OPPORTUNISTIC_DEFECTION_THRESHOLD
        and actual_window_size >= MIN_WINDOW_SIZE_FOR_OPPORTUNISTIC_DEFECTION
    ):
        choice = 0
    if defection_rate >= PUNITIVE_DEFECTION_THRESHOLD:
        choice = 0
    return choice, memory
