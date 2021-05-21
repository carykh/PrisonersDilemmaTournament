import random
from decimal import Decimal

import numpy as np

# Detective but instead of tit for tat, use nprtt


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
            num_rounds = history.shape[1]

            opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
            our_second_last_move = history[0, -2] if num_rounds >= 2 else 1

            # if opponent defects more often, then screw 'em
            MAX_DEFECTION_THRESHOLD = Decimal(1) / Decimal(2)

            opponent_history = history[1, 0:num_rounds]
            opponent_stats = dict(zip(*np.unique(opponent_history, return_counts=True)))
            opponent_defection_rate = Decimal(int(opponent_stats.get(0, 0))) / Decimal(
                num_rounds
            )

            be_patient = opponent_defection_rate <= MAX_DEFECTION_THRESHOLD

            choice = (
                1
                if (
                    opponents_last_move == 1
                    or (be_patient and our_second_last_move == 0)
                )
                else 0
            )
    return choice, shallIExploit
