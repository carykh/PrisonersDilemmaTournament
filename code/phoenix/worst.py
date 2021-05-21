import numpy as np

def strategy(history, memory):
    choice = 0
    if history.shape[1] != 0:
        percents = np.average(history, axis=1, weights=memory[::-1])
        if percents[0] > percents[1] + 0.1:
            choice = 1
        memory.append(0.85 ** len(history))
    else:
        memory = [1]
    return choice, memory
