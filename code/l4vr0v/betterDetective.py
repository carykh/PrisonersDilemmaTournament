import random

import numpy as np

# A modification of Detective. Instead of using Tit for Tat when the opponent betrays you it uses the much more agressive Forgiving Tit for Tat which will only forgive you when you are nice for two consecutive turns
#
# Better DETECTIVE: First: I analyze you. I start:
# Cooperate, Defect, Cooperate, Cooperate.
# If you defect back, I'll act like [Forgiving Tit for Tat].
# If you never defect back, I'll act like [alwaysDefect],
# to exploit you. Elementary, my dear Watson.
#  - nobody5050

# Reminder: For the history array, "cooperate" = 1, "defect" = 0


def strategy(history, memory):
    testingSchedule = ["cooperate", "defect", "cooperate", "cooperate"]
    gameLength = history.shape[1]
    shallIExploit = memory
    choice = None

    if gameLength < 4:  # We're still in that initial testing stage.
        choice = testingSchedule[gameLength]
    elif (
        gameLength == 4
    ):  # Time to analyze the testing stage and decide what to do based on what the opponent did in that time!
        opponentsActions = history[1]
        if (
            np.count_nonzero(opponentsActions - 1) == 0
        ):  # The opponent cooperated all 4 turns! Never defected!
            shallIExploit = True  # Let's exploit forever.
        else:
            shallIExploit = False  # Let's switch to Forgiving Tit For Tat.

    if gameLength >= 4:
        if shallIExploit:
            choice = "defect"
        else:
            choice = "cooperate"
            if (
                history.shape[1] >= 2 and history[1, -1] == 0 and history[1, -2] == 0
            ):  # We check the TWO most recent turns to see if BOTH were defections, and only then do we defect too.
                choice = "defect"
    return choice, shallIExploit
