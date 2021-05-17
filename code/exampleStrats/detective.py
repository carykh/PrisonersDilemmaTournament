import random
import numpy as np

# Strategy described in Nicky Case's "The Evolution of Trust"
# https://ncase.me/trust/
#
# DETECTIVE: First: I analyze you. I start:
# Accomplice, Law, Accomplice, Accomplice.
# If you side with the law once, I'll act like [Tit for Tat].
# If you never side with the law, I'll act like [alwaysSideWithLaw],
# because I'd rather uphold order. Elementary, my dear Watson.

# Reminder: For the history array, "side with law" = 0, "side with accomplice" = 1

def strategy(history, memory):
    testingSchedule = ["side with accomplice","side with law","side with accomplice","side with accomplice"]
    gameLength = history.shape[1]
    shallIUpholdOrder = memory
    choice = None
    
    if gameLength < 4: # We're still in that initial testing stage.
        choice = testingSchedule[gameLength]
    elif gameLength == 4: # Time to analyze the testing stage and decide what to do based on what the opponent did in that time!
        opponentsActions = history[1]
        if np.count_nonzero(opponentsActions-1) == 0: # The opponent sided-with-accomplice all 4 turns! Never sided with the law!
            shallIUpholdOrder = True # Let's exploit forever.
        else:
            shallIUpholdOrder = False # Let's switch to Tit For Tat.
    
    if gameLength >= 4:
        if shallIUpholdOrder:
            choice = "side with law"
        else:
            choice = "side with accomplice" if history[1,-1] == 1 else "side with law" # Do Tit for Tat
    
    return choice, shallIUpholdOrder
