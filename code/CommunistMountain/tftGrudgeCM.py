"""
Expects 2**n apologies (opponent C, this D) whenever it is betrayed (opponent D, this C), where n is the number of times
the opponent betrayed before. A compromise between titForTat and grimTrigger, where the former expects 1 apology and the
latter expects infinite apologies.

This is also the entry which I submitted.
"""


# memory[0] is the number of currently expected apologies, memory[1] is the number of apologies expected next time.
def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, [0, 1]
    elif history[1][-1] == 0 and memory[0] == 0:  # new betrayal
        memory[0] = memory[1]
        memory[1] *= 2
    elif history[1][-1] == 1 and memory[0] > 0:  # apology
        memory[0] -= 1
    if memory[0] == 0:
        return 1, memory
    else:
        return 0, memory
