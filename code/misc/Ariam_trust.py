import numpy as np
import random

def strategy(history, memory):
    choice = None
    if history.shape[1] == 0:
        choice = 0
    else:
        choice = random.choice(history[1])
    return choice, None
