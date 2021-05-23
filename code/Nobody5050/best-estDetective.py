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
    testingSchedule = [1, 0, 1, 1]
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
        elif (
            np.count_nonzero(opponentsActions - 1) == 4
        ):  # The opponent always defected... hmm... maybe they're just jerks.
            shallIExploit = True
        else:
            shallIExploit = False  # Let's switch to Forgiving Tit For Tat.

    if gameLength >= 4:
        if shallIExploit:
            choice = 0
        else:
            """
            If opponent defected, respond with defection. *UNLESS* we defected the turn before.
            - l4vr0v
            """
            opponents_last_move = history[1, -1] if history.shape[1] >= 1 else 1
            our_second_last_move = history[0, -2] if history.shape[1] >= 2 else 1
            choice = 1 if (opponents_last_move == 1 or our_second_last_move == 0) else 0
    return choice, shallIExploit
