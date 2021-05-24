import random
import numpy as np

P_forgive = .25
START_FANCY = 20

pointsArray = np.array([[1,5],[0,3]])

def strategy(history, memory):
    """
    This one assumes that every other strategy is just like the one in parametric
    Takes 20 turns to gather data, acts like parametric_1, and then exploits if
    it can...
    
    It usually can't.
    """
    if history.shape[1] == 0:
        return 1, None
    elif history.shape[1] < START_FANCY:
        return history[1, -1] or (1 if random.random() <= P_forgive else 0), None
    else:
        # This is where the fancy stuff kicks in
        ourHistory = history[0, 0:-1]
        theirResponses = history[1, 1:]
        betraySample = theirResponses[ourHistory == 0]
        allySample = theirResponses[ourHistory == 1]

        P0 = np.average(betraySample) if len(betraySample) else 0
        P1 = np.average(allySample) if len(allySample) else 1

        return np.dot(pointsArray[1], (1 - P1, P1)) >= np.dot(pointsArray[0], (1 - P0, P0)), None
