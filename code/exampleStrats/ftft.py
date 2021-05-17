# Forgiving Tit for Tat.
# Choose to defect if and only if the opponent just defected TWICE in a row.

# Reminder: For the history array, "cooperate" = 1, "defect" = 0

def strategy(history, memory):
    choice = "cooperate"
    if history.shape[1] >= 2 and history[1,-1] == 0 and history[1,-2] == 0: # We check the TWO most recent turns to see if BOTH were defections, and only then do we defect too.
        choice = "defect"
    return choice, None
