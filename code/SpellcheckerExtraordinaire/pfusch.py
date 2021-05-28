import random
import numpy as np

# Pfusch, german for "botch"
# That is because I was made aware of this challenge mere hours before its conclusion, so botching is the best I can do, especially since I'm not great at statistics
# The idea: Can I create a model of my opponent's decision probabilities and simulate them in the future to determine the best results for me?
# Works well against strategies with simple decision models and terribly against random strategies

PREDICTION_HORIZON = 8 # As you said you read the code before executing, if this strategy should be too slow to be qualified feel free to reduce this number, as the runtime is 2^PREDICTION_HORIZON just subtracting one should do the trick
RANDOM_TIME = 7 # how long to do random stuff

# shamelessly stolen
pointsArray = [[1,5],[0,3]] # The i-j-th element of this array is how many points you receive if you do play i, and your opponent does play j.
def tallyRoundScores(history):
    scoreA = 0
    scoreB = 0
    ROUND_LENGTH = history.shape[1]
    for turn in range(ROUND_LENGTH):
        playerAmove = history[0,turn]
        playerBmove = history[1,turn]
        scoreA += pointsArray[playerAmove][playerBmove]
        scoreB += pointsArray[playerBmove][playerAmove]
    return scoreA/ROUND_LENGTH, scoreB/ROUND_LENGTH

# given the history, what is the total probability of my opponent choosing 0
def totalProb(history):
    zeroCount = 0
    for choice in history[1]:
        if choice == 0:
            zeroCount = zeroCount + 1

    zeroProb = zeroCount / history.shape[1]

    return zeroProb

# can I figure out how my choices influence my opponent?
def calcInfluence(history):
    gameLength = history.shape[1]

    influences = (0, 1, 0, 1, 0.5)
    for i in range(1, gameLength):
        truncatedHistory = history[:, :i]
        curProb = totalProb(truncatedHistory)
        influences = calcInfluenceIncrement(influences, history[0,i-1], curProb)

    return influences 

# how did the total chance of the opponent choosing 0 change given my action of the last round
def calcInfluenceIncrement(prevInfluences, choice, curProb):
    (zeroChanceIncrease, zeroCount, oneChanceIncrease, oneCount, prevProb) = prevInfluences
    diff = curProb - prevProb
    if choice == 0:
        zeroCount = zeroCount + 1
        zeroChanceIncrease = zeroChanceIncrease + diff
    else:
        oneCount = oneCount + 1
        oneChanceIncrease = oneChanceIncrease + diff

    return (zeroChanceIncrease, zeroCount, oneChanceIncrease, oneCount, curProb)

# build a tree of all my possible decisions, PREDICTION_HORIZON steps into the future
# take the choice that will lead me to the path with the greatest expected outcome
# is stupidly slow, makes 2^PREDICTION_HORIZON recursive calls
def forwardSimulate(influences, history, count):
    if count == PREDICTION_HORIZON:
        return tallyRoundScores(history), 0

    (zeroChanceIncrease, zeroCount, oneChanceIncrease, oneCount, prevProb) = influences

    opponentChoice = 0
    if prevProb < 0.5:
        opponentChoice = 1

    choice0Score, _ = forwardSimulate(
            (zeroChanceIncrease, zeroCount, oneChanceIncrease, oneCount, prevProb + zeroChanceIncrease), # I add my expected change of probability given the choice I will make
            np.append(history, np.array([[0], [opponentChoice]]), axis=1), # create a mock history that includes my expectation of what will happen this round
            count + 1
        )
    choice1Score, _ = forwardSimulate(
            (zeroChanceIncrease, zeroCount, oneChanceIncrease, oneCount, prevProb + oneChanceIncrease),
            np.append(history, np.array([[1], [opponentChoice]]), axis=1),
            count + 1
        )

    if choice0Score > choice1Score:
        return choice0Score, 0
    else:
        return choice1Score, 1


def strategy(history, memory):
    gameLength = history.shape[1]
    choice = 0

    if gameLength < RANDOM_TIME: # Try random stuff, see how the opponent reacts.
        choice = random.randint(0, 1)
    elif gameLength == RANDOM_TIME: # Estimate how much my choices influence the choice of the opponent
        memory = calcInfluence(history)
        choice = random.randint(0, 1)
    else: 
        prob = totalProb(history)
        memory = calcInfluenceIncrement(memory, history[0, gameLength-1], prob)
        score, choice = forwardSimulate(memory, history, 0)
         
    return choice, memory
