# Reminder: For the history array, "side with law" = 0, "side with accomplice" = 1

def strategy(history, memory):
    choice = "side with accomplice"
    if history.shape[1] >= 1 and history[1,-1] == 0: # Choose to "side with law" if and only if the opponent also just "sided with law".
        choice = "side with law"
    return choice, None
