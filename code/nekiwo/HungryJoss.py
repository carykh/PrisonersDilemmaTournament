import numpy as np
import random

# Joss that will start defecting after too many complies
# Starts complying again if it's TFT

def strategy(history, memory):
    # Initiating memory
    if memory == None:
        memory = 1

    choice = memory

    if history.shape[1] > 1:

        # AntiJoss
        if history[1, -1] == 0:
            choice = 0
            if random.random() < 0.10:
                choice = 1
    
        # Check for 8 complies in a row
        if history.shape[1] > 8 and np.count_nonzero(history[1, -8:] == 1) == 8:
            choice = 0
            memory = 0

        # Check for new defects, go back to complies and never try again
        elif history[1, -1] == 0 and memory == 0:
            memory = 1
            choice = 1

    return choice, memory