import random

# Variant of Tit For Tat that randomly defects to try to take advantage
# of overly forgiving opponents.

def strategy(history, memory):
    choice = 1
    if (history.shape[1] >= 1 and history[1,-1] == 0):
        choice = 0
        if random.random() < 0.10:
            choice = 1
    return choice, None
