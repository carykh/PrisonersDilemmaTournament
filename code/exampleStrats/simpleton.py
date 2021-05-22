# Strategy described in Nicky Case's "The Evolution of Trust"
# https://ncase.me/trust/
#
# SIMPLETON: Hi! I try to start by cooperating. If  you cooperate
# back, I do the same thing as my last move, even if it was a mistake.
# If you defect back, I do the opposite thing as my last move, even
# if it was a mistake.

# Reminder: For the history array, "cooperate" = 1, "defect" = 0

def strategy(history, memory):
    choice = None
    if history.shape[1] == 0: # We're on the first turn!
        choice = "cooperate"
    else:
        choice = "cooperate" if history[0,-1] == 1 else "defect" # I will keep doing the same thing as last move!
        if history[1,-1] == 0: # If my opponent defected last turn, I'll just do the opposite thing as my last move:
            choice = "defect" if history[0,-1] == 1 else "cooperate" # I will keep doing the same thing as last move!
            
    return choice, None
