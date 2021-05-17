import random
import numpy as np

# Strategy described in Nicky Case's "The Evolution of Trust"
# https://ncase.me/trust/
#
# DETECTIVE: First: I analyze you. I start:
# Silent, Truth, Silent, Silent.
# If you "tell the truth", I'll act like [Tit for Tat].
# If you never "tell the truth", I'll act like [alwaysTellTruth],
# because I'd rather uphold order. Elementary, my dear Watson.

# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

def strategy(history, memory):
    testingSchedule = ["stay silent","tell truth","stay silent","stay silent"]
    gameLength = history.shape[1]
    shallIUpholdOrder = memory
    choice = None
    
    if gameLength < 4: # We're still in that initial testing stage.
        choice = testingSchedule[gameLength]
    elif gameLength == 4: # Time to analyze the testing stage and decide what to do based on what the opponent did in that time!
        opponentsActions = history[1]
        if np.count_nonzero(opponentsActions-1) == 0: # The opponent stayed silent all 4 turns! Never "told the truth"!
            shallIUpholdOrder = True # Let's exploit forever.
        else:
            shallIUpholdOrder = False # Let's switch to Tit For Tat.
    
    if gameLength >= 4:
        if shallIUpholdOrder:
            choice = "tell truth"
        else:
            choice = "stay silent" if history[1,-1] == 1 else "tell truth" # Do Tit for Tat
    
    return choice, shallIUpholdOrder
