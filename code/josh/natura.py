import random, numpy

# defect = 0, cooperate = 1

"""
hello, this is natura.py
original author is Josh#6441 on discord
this script is completely free to use and modify,
anyone may submit this strat to any tournament,
just dont change the name too drastically,
and give credit where relevant,
please.
"""

### https://discord.gg/UFswwahUYu ###

def strategy(history, memory):
    turn = history.shape[1]

    # i like working with lists going forwards
    # instead of arrays going backwards
    history = history.tolist()
    ourMoves = history[0][::-1]
    oppMoves = history[1][::-1]

    # optimism
    choice = 1

    # simple start
    if turn == 0:
        return 1, memory

    # not exactly rocket science here either
    if oppMoves[0] == 0:
        choice = 0

    # very simple de-looper
    if sum(ourMoves[0:6]) + sum(oppMoves[0:6]) < 2:
        choice = 1

    # if opponent has never cooperated, then always defect
    if sum(oppMoves) == 0:
        choice = 0
    
    # random detection, has to specifically exclude alternating strats
    if turn > 10 and abs(0.5-(sum(oppMoves) / turn )) < 0.1:
        if not ( oppMoves[0:6] == [0,1,0,1,0,1] or oppMoves[0:6] == [1,0,1,0,1,0] ):
            choice = 0
        
    # simple de-bouncer
    if turn > 6 and ourMoves[0:6] == [1,0,1,0,1,0] and oppMoves[0:6] == [0,1,0,1,0,1]:
        choice = 1
    
    # joss detector
        # yeah theres no joss detector. whoops
    
    return choice, memory
