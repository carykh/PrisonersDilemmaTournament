# Tit-for-tat, but forgiving. This is similar to antijoss, but instead of forgiving randomly, it does it predictably,
# and importantly twice in a row. This reduces the chance of getting stuck in a loop.

def strategy(history, memory):
    choice = 1
    if (history.shape[1] >= 1 and history[1, -1] == 0): # Choose to defect if and only if the opponent just defected.
        choice = 0

        if history.shape[1] % 20 < 2:
            choice = 1

    return choice, None
