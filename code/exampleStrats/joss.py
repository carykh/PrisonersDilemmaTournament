import random

# Variant of Tit For Tat that randomly defects to try to take advantage
# of overly forgiving opponents.


def strategy(history, memory):
    choice = 1
    if random.random() < 0.10 or (history.shape[1] >= 1 and history[1, -1] == 0):
        # Choose to defect randomly by 10% chance, OR if and only if the opponent just defected.
        choice = 0
    return choice, None
