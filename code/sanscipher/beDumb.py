import numpy as np


def ftft(history):
    if history.shape[1] >= 2 and history[1, -1] == 0 and history[1, -2] == 0:
        return 0
    return 1


def randomness_detector(history):
    if history.shape[1] <= 20:
        # Not enough data to consider
        return False
    deviation = 0.5 * (history.shape[1] ** 0.5)
    if abs(np.count_nonzero(history[1] == 1) - history.shape[1] * 0.5) < 2 * deviation:
        return True
    return False


def exploit_detector(history):
    try:
        if history[1, -1] == history[1, -3] and history[1, -3] == history[1, -5] and history[1, -2] == history[
                1, -4] and history[1, -2] != history[1, -1]:
            return True
    except IndexError:
        return False
    return False


def strategy(history, memory):
    turn = history.shape[1]
    if turn == 4 and np.count_nonzero(history[1] == 0) == 4:
        return 1, "Feed the Devil"
    if memory is None:
        memory = "Business as usual"
    if memory == "You dirty scammer":
        return 0, "You dirty scammer"
    if memory == "Randoms, we like":
        return 1, "Randoms, we like"
    if memory == "Feed the Devil":
        if history[1][-1] == 0:
            return 1, "Feed the Devil"
    if exploit_detector(history):
        return 0, "You dirty scammer"
    if randomness_detector(history):
        return 1, "Randoms, we like"
    if memory == "Business as usual":
        return ftft(history), "Business as usual"
