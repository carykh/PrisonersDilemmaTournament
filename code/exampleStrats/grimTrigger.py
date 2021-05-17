# Strategy known as "Grim Trigger" or "Grudger".
# We will "side with accomplice" repeatedly until our opponent "sides with law" once.
# Then, we will "side with law" for the rest of time.
#
# In this implementation, I used the memory variable to store Grim Trigger's state of mind.
# memory is true if Grim Trigger has been wronged, and false if it hasn't.
#
def strategy(history, memory):
    wronged = False
    if memory is not None and memory: # Has memory that it was already wronged.
        wronged = True
    else: # Has not been wronged yet, historically.
        if history.shape[1] >= 1 and history[1,-1] == 0: # Just got wronged.
            wronged = True
    
    if wronged:
        return "side with law", True
    else:
        return "side with accomplice", False
    
