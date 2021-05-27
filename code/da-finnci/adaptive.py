
def getScore(roundHistory):
    if getSnitchFromHistoryEntry(roundHistory[0]) and getSnitchFromHistoryEntry(roundHistory[1]):
        return 1
    elif getSnitchFromHistoryEntry(roundHistory[0]) and not getSnitchFromHistoryEntry(roundHistory[1]):
        return 5
    elif not getSnitchFromHistoryEntry(roundHistory[0]) and getSnitchFromHistoryEntry(roundHistory[1]):
        return 0
    else:
        return 3


def getSnitchFromHistoryEntry(entry):
    return entry == 0


def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"


def getGameLength(history):
    return history.shape[1]


def strategy(history, memory):
    start = [False, False, False, False, False, False, True, True, True, True, True]
    gameLength = getGameLength(history)
    if gameLength < len(start):
        snitch = start[gameLength]
    else:
        defectSum = 0
        defectCount = 0
        coopSum = 0
        coopCount = 0
        for i in range(gameLength):
            if getSnitchFromHistoryEntry(history[0,i]):
                defectSum += getScore(history[:,i])
                defectCount += 1
            else:
                coopSum += getScore(history[:, i])
                coopCount += 1
        snitch = defectSum / defectCount > coopSum / coopCount
    return getChoice(snitch), None
