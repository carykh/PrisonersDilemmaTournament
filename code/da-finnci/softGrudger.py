import numpy as np


class Memory:
    def __init__(self):
        self.numberOfDefectionsLeft = 0;
        self.numberOfCooperationsLeft = 0;

def getSnitchFromHistoryEntry(entry):
    return entry == 0


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def getGameLength(history):
    return history.shape[1]


def opponentSnitchedLastRound(history):
    return getSnitchFromHistoryEntry(history[1,-1])



def strategy(history, memory):
    if getGameLength(history) == 0:
        return getChoice(False), Memory()  # Start the duel with cooperation and initiate memory

    if memory.numberOfDefectionsLeft > 0:
        snitch = True
        memory.numberOfDefectionsLeft -= 1
    elif memory.numberOfCooperationsLeft > 0:
        snitch = False
        memory.numberOfCooperationsLeft -= 1
    elif opponentSnitchedLastRound(history):
        snitch = True
        memory.numberOfDefectionsLeft = 3
        memory.numberOfCooperationsLeft = 2
    else:
        snitch = False

    return getChoice(snitch), memory
