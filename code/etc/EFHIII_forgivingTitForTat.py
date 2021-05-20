import random

def strategy(history, memory):
    choice = 1
    if history.shape[1] >= 1 and history[1,-1] == 0 and (random.randint(0,5) > 0 or (history.shape[1] >= 2 and history[1,-2] == 0)):
        choice = 0
    return choice, None
