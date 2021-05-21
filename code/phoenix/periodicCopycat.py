WINDOW_SIZE = 5

def strategy(history, _):
    choice = 1

    if history.shape[1] != 0:
        choice = history[1, -1]

        if history.shape[1] % 20 < 2 and history[1].sum() != 0:
            choice = 1
    
    return choice, _
