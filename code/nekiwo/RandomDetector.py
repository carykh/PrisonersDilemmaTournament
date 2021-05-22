import random
import numpy as np

# Random detector(part of my private strat)
# All it does is detects random and starts pulls a defect trigger
# Best if used alongside other strats, please steal

def strategy(history, memory):
    if memory == None:
        memory = 1

    choice = memory # Use stored value 

    if history.shape[1] == 9:
        ComplyHistory = np.array(history[1, -8:]).tolist().count(1) # I don't know numpy, is this how you do it lol?
        if ComplyHistory > 2 and ComplyHistory < 8: # Super easy way of doing it, works good enough
            # It's random, activate trigger and start defecting
            choice = 0
            memory = 0

    return choice, memory