"""
After an apology from the opponent (they play C while it plays D, only happens when they play D first), if the opponent
immediately plays D, it plays another C instead of punishing in order to encourage the opponent to get back to CC-chain
(i.e. olive branch). The opponent must then play n times of C, n starts at 1 and increases by 1 every apology cycle, in
order to "prove their willingness for good relations". Otherwise, it goes full D (grudge strategy). As long as the
opponent only plays D when good relations are proven, this will require only 1 apology (titForTat strategy).
"""


# memory[0] and memory[1] help decide whether or not to do the olive branch procedure. memory[0] counts the number of
# 'good relations' needed after the extension of the olive branch, and memory[1] is the number of 'good relations'
# needed after the next olive branch extension, if it happens. memory[2] is True when it has entered 'spam D' mode
def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, [0, 1, False]
    elif history[1][-1] == 0 and history[0][-1] == 1:  # new betrayal
        if history.shape[1] > 2 and history[0][-2] == 0:  # just exited apology cycle
            return 1, [memory[1], memory[1] + 1, False]
        elif memory[0] > 0:  # betrayed during the 'good relations' period
            memory[2] = True
    elif history[1][-1] == 1 and memory[0] > 0:
        memory[0] -= 1
    if memory[2]:
        return 0, memory
    return history[1][-1], memory
