def strategy(history, memory):
    choice = 1
    if history.shape[1] >= 2 and history[1,-2] == 0: # Choose to defect if and only if the opponent defected two turns ago.
        choice = 0
    return choice, None