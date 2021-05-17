# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

# Forgiving Tit for Tat.
# Choose to tell the truth if and only if the opponent just told the truth TWICE in a row.
def strategy(history, memory):
    choice = "stay silent"
    if history.shape[1] >= 2 and history[1,-1] == 0 and history[1,-2] == 0: # We check the TWO most recent turns to see if BOTH were truth-tellings, and only then do we also tell the truth.
        choice = "tell truth"
    return choice, None
