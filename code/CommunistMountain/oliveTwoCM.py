"""
After an apology from the opponent (they play C while it plays D, only happens when they play D first), if the opponent
immediately plays D, it plays another C instead of punishing in order to encourage the opponent to get back to CC-chain
(i.e. olive branch). If it plays D in this turn or the next one, go full D.

Difference between oliveOneCM is that it requires 2 turns of good relations instead of 1.
"""


# memory[0] is 2 or 1 if it is currently doing the olive branch procedure, memory[1] is true if it is playing all D.
def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, [0, False]
    elif history[1][-1] == 0 and history[0][-1] == 1:  # new betrayal
        if history.shape[1] > 2 and history[0][-2] == 0:  # just exited apology cycle
            return 1, [2, False]
        elif memory[0] > 0:  # betrayed during the 'good relations' period
            memory[1] = True
    elif history[1][-1] == 1 and memory[0] > 0:
        memory[0] -= 1
    if memory[1]:
        return 0, memory
    return history[1][-1], memory
