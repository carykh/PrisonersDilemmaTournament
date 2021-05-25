import random

P = (.25, 1)

def strategy(history, memory):
    """
    I am trying to model strategies as taking the last action, and allying with
    a certain probability if the opponent allied, and with another if the
    opponent betrayed

    In my testing in a different environment, this was the best pair of
    parameters I have found for it.
    These set of parameters are like antijoss, just even more forgiving.
    """

    if history.shape[1]:
        opponentAction = history[1, -1]
    else:
        opponentAction = 1
    

    return random.random() <= P[opponentAction], None

