# Reminder: For the history array, "cooperate" = 1, "defect" = 0

def strategy(history, memory):
    choice = "cooperate"
    if history.shape[1] >= 1 and history[1,-1] == 0: # Choose to defect if and only if the opponent just defected.
        choice = "defect"
    return choice, None
