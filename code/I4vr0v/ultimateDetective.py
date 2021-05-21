from decimal import Decimal
import random

import numpy as np


# Detective, except:
# - use nprtt instead of tit-for-tat for the forgiveness heuristic
# - detect ftft and spam DCDCDCDCDC to take advantage of it
# - detect alwaysCooperate and spam DDDDD to take advantage of it, at the cost of the
#   grimTrigger
def strategy(history, memory):
    """
    :history: 2d numpy array of our and opponent past moves
    :memory: mode string, which may be None, 'tit-for-tat', 'alternate', or 'defect'
    """
    num_rounds = history.shape[1]
    testing_schedule = [1, 0, 0, 1, 1]
    max_defection_threshold = Decimal(1) / Decimal(2)  # do not forgive high defections

    if num_rounds < len(testing_schedule):  # intitial testing phase
        choice = testing_schedule[num_rounds]
    elif num_rounds == len(testing_schedule):  # time to transition to our modes
        opponent_moves = history[1]
        opponent_stats = dict(zip(*np.unique(opponent_moves, return_counts=True)))
        if opponent_stats.get(0, 0) < 1:  # they never defected, take advantage of them
            choice = 0
            memory = "defect"
        elif opponent_stats.get(0, 0) == len(testing_schedule):  # they always defect
            choice = 0
            memory = "defect"
        elif opponent_moves[2] == 1 and opponent_moves[3] == 0:  # ftft detected
            choice = 0
            memory = "alternate"
        else:
            choice = 1
            memory = "tit-for-tat"
    else:  # num_rounds > len(testing_schedule)
        if memory == "defect":
            choice = 0
            memory = "defect"
        elif memory == "alternate":
            our_last_move = history[0, -1] if num_rounds > 0 else 1
            choice = 0 if our_last_move else 1
            memory = "alternate"
        else:  # tit-for-tat or None
            opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
            our_second_last_move = history[0, -2] if num_rounds >= 2 else 1
            opponent_history = history[1, 0:num_rounds]
            opponent_stats = dict(zip(*np.unique(opponent_history, return_counts=True)))
            opponent_defection_rate = Decimal(int(opponent_stats.get(0, 0))) / Decimal(
                num_rounds
            )

            be_patient = opponent_defection_rate <= max_defection_threshold

            choice = (
                1
                if (
                    opponents_last_move == 1
                    or (be_patient and our_second_last_move == 0)
                )
                else 0
            )
            memory = "tit-for-tat"

    return choice, memory
