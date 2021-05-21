import random
import numpy as np

def strategy(history, bad):
    choice = 1

    if history.shape[1] == 0:
        return 1, 0

    # Enemy just defected
    if history[1, -1] == 0:
        bad += 1
        choice = 0
    elif bad > history[0].sum():
        choice = 0
    else:
        choice = random.choice(history[1, -7:])

    return choice, bad
