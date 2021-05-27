import numpy as np


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def getGameLength(history):
    return history.shape[1]



def strategy(history, memory):
    gameLength = getGameLength(history)
    if gameLength == 0:
        snitch = False
    else:
        snitch = np.amin(history[1,-min(gameLength,3):]) == 0
    return getChoice(snitch), None
