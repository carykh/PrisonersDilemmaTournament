# Reminder: For the history array, "side with law" = 0, "side with accomplice" = 1

# Forgiving Tit for Tat.
# Choose to side with law if and only if the opponent just sided with the law TWICE in a row.
def strategy(history, memory):
    choice = "side with accomplice"
    if history.shape[1] >= 2 and history[1,-1] == 0 and history[1,-2] == 0: # We check the TWO most recent turns to see if BOTH were law-sidings, and only then do we side with the law too.
        choice = "side with law"
    return choice, None
