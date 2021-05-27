#
# AGENT
# Sanjin
#
# STRATEGY
# This agent always defects, if the opponent defected too often. Otherwise it cooperates.
#

def getGameLength(history):
    return history.shape[1]


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def strategy(history, memory):
    if getGameLength(history) == 0:
        return getChoice(False), None
    average = sum(history[1]) / history.shape[1]
    snitch = average <= 0.3  # Defect if the opponent defected > 30% of times
    return getChoice(snitch), None
