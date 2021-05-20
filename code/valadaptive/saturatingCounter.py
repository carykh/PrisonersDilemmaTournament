# Implements a 2-bit saturating counter

def strategy(history, memory):
    if memory is None:
        memory = 2
    
    lastOpponentDecision = history[1][-1] if history.shape[1] >= 1 else 0
    memory += -1 if lastOpponentDecision == 0 else 1
    memory = max(0, min(memory, 3))
    choice = 1 if memory > 1 else 0
    return choice, memory