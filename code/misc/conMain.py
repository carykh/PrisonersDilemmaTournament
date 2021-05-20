import numpy


def strategy(history, memory):
    """
    Con-man strategy: build trust via tit-for-tat... but if they've been nice to us
    5 times in a row, defect opportunistically (to take advantage of simpletons).
    But don't go overboard - don't cheat repeatedly.
    """
    choice = 1
    num_rounds = history.shape[1]
    if num_rounds >= 1 and history[1, -1] == 0:
        # accept justice if they defected to punish us
        if num_rounds >= 2 and history[0, -2] == 0 and history[1, -2] == 1:
            choice = 1
        else:
            choice = 0
    elif num_rounds >= 1 and history[0, -1] == 0:
        choice = 1  # if we cheated them, don't cheat them twice
    elif num_rounds >= 5:
        last_five = history[1, num_rounds - 5 : num_rounds]
        counts = dict(zip(*numpy.unique(last_five, return_counts=True)))
        if counts.get(1, 0) == 5:
            choice = 0

    return choice, None
