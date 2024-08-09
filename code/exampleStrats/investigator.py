import random
import numpy as np

# Investigator strategy
# On the first twenty-four turns, goes through the eight possible trios of moves.
# Then, for each twenty-four turns after that, plays those moves in a random order.
# The best strat from the previous go-through gets boosted by 1, and the worst gets removed.
#
# By Aquateraneal

def strategy(history, memory):
    gamelen = history.shape[1]
    if not gamelen % 24:
        pass
