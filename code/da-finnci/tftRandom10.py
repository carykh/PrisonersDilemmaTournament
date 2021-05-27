import random

def getSnitchFromHistoryEntry(entry):
    return entry == 0


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def opponentSnitchedLastRound(history):
    return getSnitchFromHistoryEntry(history[1,-1])


def strategy(history, memory):
    snitch = False if history.shape[1] == 0 else opponentSnitchedLastRound(history)
    if random.random() < 0.10:
        snitch = not snitch
    return getChoice(snitch), None
