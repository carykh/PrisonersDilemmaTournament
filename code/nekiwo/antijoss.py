import random

# Joss but it forgives instead

def strategy(history, memory):
    choice = 1
    if history.shape[1] >= 1 and history[1, -1] == 0:
        choice = 0
        if random.random() < 0.10:
            choice = 1
    return choice, None
