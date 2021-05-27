import numpy as np


def getSnitchFromHistoryEntry(entry):
    return entry == 0


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def getGameLength(history):
    return history.shape[1]


def opponentSnitchedLastRound(history):
    return getSnitchFromHistoryEntry(history[1,-1])

def numberOfOpponentCooperations(history):
    return np.sum(history[1])

def strategy(history, memory):
    if getGameLength(history) == 0:
        snitch = False
    else:
        snitch = numberOfOpponentCooperations(history) < getGameLength(history) - numberOfOpponentCooperations(history)
    return getChoice(snitch), None
