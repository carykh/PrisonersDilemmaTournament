# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

def strategy(history, memory):
    choice = "stay silent"
    if history.shape[1] >= 1 and history[1,-1] == 0: # Choose to "tell the truth" if and only if the opponent also just "told the truth".
        choice = "tell truth"
    return choice, None
