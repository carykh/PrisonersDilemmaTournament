import numpy as np
import random

alwaysdefect = lambda history: 0

def joss(history):
    if history[1, -1] == 0: 
        if history[0, -1] != 0:
            return 0
    if random.random() >= 0.8:
        return 0
    return 1

def strategy(history, strat):
    start_seq = [1,0,1,1,1]
    if history.shape[1] <= 4:
        return start_seq[history.shape[1]], None

    if history.shape[1]%5 == 0:
        observations = np.flip(history[:, -1:-6:-1], axis=1)
        if np.all(observations[1]==0) or np.all(observations[1]==1):
            strat = alwaysdefect
        elif np.all(observations[1, ::2] == observations[1, ::2][0]) and np.all(observations[1, 1::2] == observations[1, 1::2][0]):
            strat = alwaysdefect
        elif np.all(observations[1, 1:] == 0):
            strat = alwaysdefect
        else:
            tft_check = []
            for i in range(observations.shape[1]):
                if observations[1, i] == 0:
                    if i == 0 and history.shape[1] == 5:
                        tft_check.append(False)
                    else:
                        if history[0, -6+i] == 0:
                            tft_check.append(True)
                        else:
                            tft_check.append(False)
                        
            if len([i for i in tft_check if i == True])/len(tft_check) >= 0.6:
                strat = joss
            else:
                strat = alwaysdefect

    return strat(history), strat   
    
