import numpy as np

def strategy(history, memory):
    n = history.shape[1]
    if n == 0:
        return 1, np.array([0] * 16)
    elif n >= 2:
        olderMove = 2 * history[0, -2] + history[1, -2]
        recentMove = 2 * history[0, -1] + history[1, -1]
        memory[4 * olderMove + recentMove] += 1

    # measure the amount of uncertainty in sequence
    with_data = memory[np.where(memory > 0)] / n
    entropy = -1 * np.sum(with_data * np.log(with_data) / np.log(16))
    if entropy > 0.7:
        return 0, memory  # 'tis probably random

    # tit for tat
    # with periodic forgiveness (CC) if they've cooperated at least 5% of the time
    # and their defection is a response to our defection
    if n >= 1 and history[1, -1] == 0:
        if n % 16 < 2 and n > 2 and np.sum(history[1]) / n > 0.05 and history[0, -2] == 0:
            return 1, memory
        return 0, memory
    return 1, memory