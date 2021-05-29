"""
After an apology cycle is complete (they play C while it plays D, until we are satisfied), if the opponent immediately
plays D, it plays another C instead of punishing in order to encourage the opponent to get back to CC-chain
(i.e. olive branch). The next time the opponent betrays, expect 2 apologies, otherwise expect 1.
"""


# memory[0] is number of required apologies, memory[1] is True if olive branch is active (+1 apology next time)
def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, [0, False]
    elif history[1][-1] == 0 and history[0][-1] == 1:  # new betrayal
        if history.shape[1] > 2 and history[0][-2] == 0:  # just exited apology cycle
            return 1, [0, True]
        elif memory[1]:  # betrayed while olive branch is active
            return 0, [2, False]
        else:
            return 0, [1, False]
    elif history[1][-1] == 1 and memory[0] > 0:
        memory[0] -= 1
    if memory[0] > 0:
        return 0, memory
    else:
        return 1, memory
