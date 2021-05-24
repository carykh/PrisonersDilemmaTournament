import random
import numpy as np

# My detective strat, V1

# First it starts detecting random and fixes itself when it realizes its joss
# If the opponent isnt random, it just does AntiJoss
# Right before the end it aggressively goes nuts

# Config
window = 8

# Detecting
class detection:

    def random(history, IsRandom):
        ComplyHistory = np.count_nonzero(history[1, -window:] == 1)
        if ComplyHistory > 3 and ComplyHistory < 5: # Super easy way of doing it, works good enough
            # It's random
            IsRandom = True

        return IsRandom


    def tft(history, IsTFT, IsRandom):
        DefectHistory = np.count_nonzero(history[1, -window:] == 1)

        if DefectHistory < np.floor(window / 3): # Helps with AntiJoss detection
            # Oof, it's TFT/Joss
            IsTFT = True
            IsRandom = False

        return IsTFT, IsRandom


# Doing strats
class strat:

    def AntiJoss(history):
        choice = 1
        if history.shape[1] >= 1 and history[1, -1] == 0:
            choice = 0
            if random.random() < 0.10:
                choice = 1
        return choice

    def GameEndAbuse():
        
        return 1


def strategy(history, memory):

    # Some memory variables
    IsRandom = False
    IsTFT = False

    choice = strat.AntiJoss(history) # Default choice is AntiJoss

    # Initiating memory
    if memory == None:
        # Memory variables in array:
        memory = [
                IsRandom, # 0
                IsTFT     # 1
            ]
    else:
        IsRandom = memory[0]
        IsTFT = memory[1]
            

    # Enemy analyzis:

    # Detect random
    if history.shape[1] == window + 1:
        RandomDetector = detection.random(history, IsRandom)
        IsRandom = RandomDetector


    # Check if the "random" is actually Joss and revert back if it is
    elif history.shape[1] == window * 2 + 1 and IsRandom:
        TFTDetector = detection.tft(history, IsTFT, IsRandom)
        IsTFT = TFTDetector[0]
        IsRandom = TFTDetector[1]

        if not IsTFT:
            choice = 0
            
    # If not random, start AntiJoss
    elif history.shape[1] > window + 1:
        choice = strat.AntiJoss(history)

    # Defect if random
    if history.shape[1] > window and IsRandom:
        choice = 0





    # Saving memory variables before the next move
    memory = [IsRandom, IsTFT]

    return choice, memory