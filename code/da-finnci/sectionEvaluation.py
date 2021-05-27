import numpy as np

#
# AGENT
#  Section Evaluation Agent
#
# INTRODUCTION
# This agent follows the principles of the normal TFT agent, but tries to improve on possible weaknesses.
#
# STRATEGY
# The agent checks sections at the end of the history of increasing size (powers of 2),
# to check if the opponent breached trust more than half of the times in the section.
# If the opponent did this in any section, then this agent will defect.
#
# As a result short term it will look like TFT.
# On a larger timescale this agent is less friendly though, if it encounters repeated breach of trust.
# This should help against random playing opponents whom TFT trusts unnessecarily much.
#
# There is also a special pattern recognition: If the opponent at some point defects but later follows TFT,
# a revenge cycle is possible. This agent can detect and break it.
#

def getSnitchFromHistoryEntry(entry):
    return entry == 0


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def getGameLength(history):
    return history.shape[1]


def opponentSnitchedLastRound(history):
    return getSnitchFromHistoryEntry(history[1,-1])

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def isHistoryBad(history, numberOfRoundsToCheck):
    total = 0
    for i in range(numberOfRoundsToCheck):
        if getSnitchFromHistoryEntry(history[1, -(i+1)]):
            total += 1
    return total/numberOfRoundsToCheck > 0.5

def isInRevengeCycle(history):
    pattern = np.array([[0, 1, 0, 1], [1, 0, 1, 0]])
    return getGameLength(history) >= pattern.shape[1] and np.array_equal(history[:,-4:], pattern)

def strategy(history, memory):
    snitch = False
    i = 0
    while pow(2,i) <= getGameLength(history) and not snitch:
        snitch = isHistoryBad(history, pow(2,i))
        i += 1

    if isInRevengeCycle(history):
        snitch = False

    return getChoice(snitch), None
