import random
import numpy as np

def strategy(history, _):
    choice = 1

    if history.shape[1] != 0:
        # Enemy just defected
        if history[1, -1] == 0:
            choice = 0
            if history.shape[1] % 20 < 2:
                choice = 1
        else:
            start = history.shape[1] - 4
            end = history.shape[1]
            random.choice(history[1, start:end])

    return choice, _
