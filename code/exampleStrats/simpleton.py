# Strategy described in Nicky Case's "The Evolution of Trust"
# https://ncase.me/trust/

# Reminder: For the history array, "side with law" = 0, "side with accomplice" = 1

# SIMPLETON: Hi! I try to start by "siding with accomplice". If you "side with accomplice"
# back, I do the same thing as my last move, even if it was a mistake.
# If you "side with law" back, I do the opposite thing as my last move, even
# if it was a mistake.

def strategy(history, memory):
    choice = None
    if history.shape[1] == 0: # We're on the first turn!
        choice = "side with accomplice"
    else:
        choice = "side with accomplice" if history[0,-1] == 1 else "side with law" # I will keep doing the same thing as last move!
        if history[1,-1] == 0: # If my opponent "sided with law" last turn, I'll just do the opposite thing as my last move:
            choice = "side with law" if history[0,-1] == 1 else "side with accomplice"
            
    return choice, None
