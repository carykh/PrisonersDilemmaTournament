import random, numpy

# defect = 0, cooperate = 1 #

"""
presto.py
original author is Josh#6441 on discord
at the core of this strategy is omega tit for tat, outlined here:
https://arxiv.org/ftp/cs/papers/0609/0609017.pdf
i have modified omega with some logic i created myself,
which makes it more capable of dealing with a wider range of opponents,
while still taking advantage of omega's highly accurate random detection
currently, i have balanced it to more accurately detect joss-likes,
at the expense of some of its random detection speed
"""

### https://discord.gg/UFswwahUYu ###

def strategy(history, memory):

    # i like working with lists going forwards
    # instead of arrays going backwards
    turn = history.shape[1]
    history = history.tolist()
    ourMoves = history[0][::-1]
    oppMoves = history[1][::-1]

    if turn == 0:
        return 1, (0,0)

    # we begin the sus counter higher if the opponent defected on their first move
    # while not many strategies will do this, randoms will do it 50% of the time
    # this increases the rate of random detection
    if turn == 1:
        return 1, (0,(1-oppMoves[0])*5,[0])  

    loopCounter,susCounter,udr = memory

    # omega code begins here

    if loopCounter > 2:
        choice = 1

        if loopCounter == 3:
            loopCounter += 1

        else:
            loopCounter = 0
            
    else:

        if oppMoves[0] == 1 and oppMoves[1] == 1:
            susCounter -= 1.5

        if oppMoves[0] != oppMoves[1]:
            susCounter += 1.25 

        if oppMoves[0] != ourMoves[1]:
            susCounter += 1.5

        if susCounter > 7:
            choice = 0

        else:

            choice = oppMoves[0]

            if oppMoves[0] != oppMoves[1]:
                loopCounter += 1

            else:
                loopCounter = 0

    # omega code ends here

    # joss detector. uses udr (unprovoked defection rate)
    if turn > 30 and len(udr)/turn < 0.15 and turn-udr[len(udr)-1] < 10:
        if susCounter < 5:
            choice = 1

    # updates the udr
    if oppMoves[0] == 0 and ourMoves[1] == 1:
       udr.append(turn)

    # this does something helpful, dont know why. last minute addition
    if turn > 10 and oppMoves[0:2] == [1,0] and ourMoves[0:2] == [1,1]:
        susCounter = 0
        choice = 1

    # de-looping code. does a check for statistical randomness,
    # to prevent de-looping against a random opponent
    if sum(ourMoves[0:6]) + sum(oppMoves[0:6]) < 2:
        if turn < 10 or abs(0.5-(sum(oppMoves) / turn )) > 0.1:
            choice = 1

    # if opponent has defected for many turns in a row, then defect
    if sum(oppMoves[0:15]) == 0:
        choice = 0

    return choice, (loopCounter,susCounter,udr)
