# Strategy described in Nicky Case's "The Evolution of Trust"
# https://ncase.me/trust/

# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

# SIMPLETON: Hi! I try to start by "staying silent". If you "stay silent"
# back, I do the same thing as my last move, even if it was a mistake.
# If you "tell the truth" back, I do the opposite thing as my last move, even
# if it was a mistake.

def strategy(history, memory):
    choice = None
    if history.shape[1] == 0: # We're on the first turn!
        choice = "stay silent"
    else:
        choice = "stay silent" if history[0,-1] == 1 else "tell truth" # I will keep doing the same thing as last move!
        if history[1,-1] == 0: # If my opponent "told the truth" last turn, I'll just do the opposite thing as my last move:
            choice = "tell truth" if history[0,-1] == 1 else "stay silent"
            
    return choice, None
