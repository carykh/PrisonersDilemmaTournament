import numpy as np
from math import inf

"""
Strategy made by duckboycool for carykh's Prisoner's Dilemma Tournament. (https://youtu.be/r2Fw_rms-mA)

It is a nice Tit for Tat based strategy that attempts to detect when the opponent is not changing their actions based
off of ours so we can maximize with defects, and attempts to cooperate extra in certain scenarios to avoid defection chains.
"""

# Non-responsive factor sensitivities
deafThresh = 0.37
deafThresh2 = 0.13

patterns = [
    (np.array([[],[]], dtype=int), (True, None)), # Start (cooperate)

    (np.array([[True, False, True], # Defection chain
               [False, True, False]], dtype=int), (True, None)), # Cooperate extra to try to get out (max of 9)
    
    (np.array([[True, False, True, False, True], # Longer defection chain (if first is at max)
               [False, True, False, True, False]], dtype=int), (True, None)), # Cooperate extra to try to get out (max of 4)

    (np.array([[True, False, False, True, False, False, True, False], # Other defection chain
               [False, False, True, False, False, True, False, False]], dtype=int), (True, [True, True])), # Cooperate a lot extra to try to get out (max of 3)
    
    (np.array([[True, False, True], # They didn't respond to retaliation (possibly forgiving despite also testing?)
               [False, True, True]], dtype=int), (False, None)), # Defect again to see how they react
    
    (np.array([[True, False, True, False, False, False], # Forgiving, but retaliating after 2
               [True, True, True, True, True, False]], dtype=int), (True, [False, True])), # Defect every other (and don't detect random, max of 6)

    (np.array([[True, False, True], # No response to defection (probably forgiving)
               [True, True, True]], dtype=int), (False, None)), # Defect to take advantage of forgiveness

    (np.array([[False, False, False], # No response to defection
               [True, True, True]], dtype=int), (False, [False])), # Defect a few times to take advantage
    
    (np.array([[False, False, False, False], # Inconsistent defection
               [True, True, False, True]], dtype=int), (False, [False])), # Defect (expected of >3, max of 6)
    
    (np.array([[False, False, False, False], # Defected inconsistently to defection
               [False, True, True, True]], dtype=int), (False, [False])), # Defect (expected of >3, max of 2)

    (np.array([[True, True, False, True, True, True], # Tried defecting
               [True, False, True, False, True, True]], dtype=int), (False, None)), # Defect to test (since they're non-nice anyway, max of 2)

    (np.array([[True, False, True, True, True, False], # Alternating
               [False, True, False, True, False, True]], dtype=int), (False, [False])), # Defect (non-responsive potentially, max of 7)
]

counts = []
maxes = [inf, 9, 4, 3, inf, 6, inf, inf, 6, 2, 2, 7]

defects = np.array([[False, False, False, False],
                    [False, False, False, False]], dtype=int)

def strategy(history, memory):
    if not(history.size):
        counts.clear()

        for x in patterns:
            counts.append(0)

    if memory: # Do sequence given in memory
        return memory.pop(0), memory

    for i, (pattern, response) in enumerate(patterns):
        if counts[i] < maxes[i]:
            if history.size >= pattern.size and np.array_equal(pattern, history[:,-pattern.shape[1]:]):
                counts[i] += 1

                return response

    # Non-responsive detection
    responses = np.array([history[0,:-1], history[1,1:]], int)
    Ts = np.where(responses[0] == True)[0]
    Fs = np.where(responses[0] == False)[0]

    TtT = np.count_nonzero(responses[1][Ts])
    TtF = np.count_nonzero(np.logical_not(responses[1][Ts]))
    FtT = np.count_nonzero(responses[1][Fs])
    FtF = np.count_nonzero(np.logical_not(responses[1][Fs]))

    if (
        len(Ts) > 2 and len(Fs) > 3 and counts[5] == 0 and # Enough sample (and haven't already tried against forgiving)
        (((abs(TtT - TtF)/len(Ts)) < deafThresh and (abs(FtT - FtF)/len(Fs)) < deafThresh) or # Sensed not responding (low ratios)
        abs(TtF/len(Ts) - FtF/len(Fs)) < deafThresh2) # Sensed not responding (similar ratios)
       ): # Probably non-responsive (random, or following a set pattern)
        return False, None # Defect since they won't retaliate

    if np.array_equal(history[:,-4:], defects) and (True in history[1,-22:]): # All defections recently and player has cooperated somewhat recently (or currently close to start)
        return True, [True, True] # Cooperate now and next 2 turns, try to avoid all defections if possible
    
    return history[1,-1], None # Tit for Tat
  
