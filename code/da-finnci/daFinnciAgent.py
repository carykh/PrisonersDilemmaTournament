import numpy as np

#
# AGENT
# da Finnci agent
#
# INTRODUCTION
# This agent is based on Tit for Tat, but has a number of special behaviours implemented for different scenarios.
#
# STRATEGY
# Normally the agent follows Tit for Tat.
#
# If the opponent at some point defects but later follows TFT, a revenge cycle is possible.
# This agent can detect and break it.
#
# If a total war takes place - both parties keep defecting - then this agent makes a strong effort to break it.
# If unsuccessful the attempt will be repeated at increasing intervals.
#
# If the opponent often answers with defecting to friendly behaviour this agent starts a strict punishment.
# This is a countermeasure against randomness.
#

DEESCALATION_ATTEMPT_INTERVALS = [3, 9, 27]
LIMIT_FOR_PUNISHMENT = 0.3
COOPERATION_MIN_COUNT = 10


class Memory:
    def __init__(self):
        self.cooperationsAnsweredByDefecting = 0;
        self.cooperations = 0;
        self.deescalationAttempts = 0


def getSnitchFromHistoryEntry(entry):
    return entry == 0


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def getGameLength(history):
    return history.shape[1]


def opponentSnitchedLastRound(history):
    return getSnitchFromHistoryEntry(history[1,-1])


def isInRevengeCycle(history):
    pattern = np.array([[0, 1, 0, 1], [1, 0, 1, 0]])
    length = pattern.shape[1]
    return getGameLength(history) >= length and np.array_equal(history[:,-length:], pattern)


def startDeescalationAttempt(history, memory):
    if memory.deescalationAttempts == len(DEESCALATION_ATTEMPT_INTERVALS):
        return False
    interval = DEESCALATION_ATTEMPT_INTERVALS[memory.deescalationAttempts]
    return getGameLength(history) >= interval and np.amax(history[:,-interval:]) == 0


def ongoingDeescalationAttempt(history):
    pattern = np.array([[0, 0, 0, 1], [0, 0, 0, 0]])
    length = pattern.shape[1]
    return getGameLength(history) >= length and np.array_equal(history[:,-length:], pattern)

def deescalationAttemptSuccessful(history):
    pattern = np.array([0, 0, 0, 1, 1])
    length = pattern.shape[0]
    return not opponentSnitchedLastRound(history) and np.array_equal(history[0, -length:], pattern)

def writeCooperationResponseToMemory(history, memory):
    if getGameLength(history) > 1 and not getSnitchFromHistoryEntry(history[0, -2]):
        memory.cooperations += 1
        if opponentSnitchedLastRound(history):
            memory.cooperationsAnsweredByDefecting += 1


def punishUnfriendlyResponses(memory):
    return memory.cooperations >= COOPERATION_MIN_COUNT and memory.cooperationsAnsweredByDefecting / memory.cooperations > LIMIT_FOR_PUNISHMENT


def strategy(history, memory):
    if getGameLength(history) == 0:
        return getChoice(False), Memory()  # Start the duel with cooperation and initiate memory

    snitch = opponentSnitchedLastRound(history)  # Tit for Tat
    if not snitch:
        memory.deescalationAttempts = max(0, memory.deescalationAttempts-1)  # Opponent cooperated, deescalation successful

    if deescalationAttemptSuccessful(history):
        memory.cooperationsAnsweredByDefecting = 0  # Deescalation includes memory, but this is only triggered after a fully completed deescalation attempt
        memory.cooperations = 0

    writeCooperationResponseToMemory(history, memory)
    if punishUnfriendlyResponses(memory):
        memory.deescalationAttempts = max(memory.deescalationAttempts, 1)
        snitch = True  # Punish repeated breaking of trust after friendliness

    startDeescalation = startDeescalationAttempt(history, memory)
    if startDeescalation:
        memory.deescalationAttempts += 1  # Keep track of deescalation attempts

    if startDeescalation or ongoingDeescalationAttempt(history) or isInRevengeCycle(history):
        snitch = False  # Deescalation in special scenarios

    return getChoice(snitch), memory
