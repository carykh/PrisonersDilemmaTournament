# A grimTrigger and titForTat hybrd with deadlock protection from decxjo.omega

import numpy as np

FORGIVENESS = 2


def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, [False, 0]

    wronged = memory[0]
    deadlock = memory[1]

    # Punish the opponent if they defect several times in a row
    if deadlock >= 1:
        wronged = False
        if deadlock == 1:
            deadlock += 1
        else:
            deadlock = 0
    elif (history.shape[1] >= FORGIVENESS
          and history[1, -FORGIVENESS:].sum() == 0
          and np.count_nonzero(history[0, -FORGIVENESS:] - 1) == 0):
        wronged = True
    # Forgive the opponent if they cooperate several times in a row
    elif (history.shape[1] >= FORGIVENESS * 2
          and np.count_nonzero(history[1, -FORGIVENESS*2:] - 1) == 0):
        wronged = False
    elif history.shape[1] >= 2:
        if history[1, -1] != history[1, -2]:
            deadlock += 1
        else:
            deadlock = 0

    memory = [wronged, deadlock]

    # grimTrigger
    if wronged:
        return 0, memory
    # periodic titForTat
    elif history.shape[1] >= 1 and history[1, -1] == 0:
        if history.shape[1] % 20 < 2 and history[1].sum() != 0:
            return 1, [False, deadlock]
        return 0, memory
    # coop
    else:
        return 1, memory
