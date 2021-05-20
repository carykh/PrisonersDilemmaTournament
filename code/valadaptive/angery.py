# Betray our opponent more the more they betray us.

def strategy(history, anger):
    if anger is None:
        anger = 0
    if history.shape[1] >= 1 and history[1, -1] == 0:  # Just got wronged.
        anger += 2
    
    anger = max(0, anger - 1)

    choice = 0 if anger > 0 else 1

    return choice, anger
