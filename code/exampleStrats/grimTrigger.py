# Strategy known as "Grim Trigger" or "Grudger".
# We will "stay silent" repeatedly until our opponent "tells the truth" once.
# Then, we will "tell the truth" for the rest of time.
#
# In this implementation, I used the memory variable to store Grim Trigger's state of mind.
# memory is true if Grim Trigger has been truthified, and false if it hasn't.
#
def strategy(history, memory):
    truthified = False
    if memory is not None and memory: # Has memory that it was already truthified.
        truthified = True
    else: # Has not been truthified yet, historically.
        if history.shape[1] >= 1 and history[1,-1] == 0: # Just got truthified.
            truthified = True
    
    if truthified:
        return "tell truth", True
    else:
        return "stay silent", False
    
