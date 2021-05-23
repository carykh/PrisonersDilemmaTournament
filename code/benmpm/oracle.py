# courtesy of benmpm
import numpy as np

# Aaronson's Oracle + other strategies
# https://github.com/elsehow/aaronson-oracle

N = 3
# Multiplier for learn weight every round
LEARN_RATE = 0.85
# Minimum confidence to guess co-op
MIN_CONFIDENCE = 0.80
naughtiness = 0.05
last_prediction = 0
predictions = 0
correct = 0
n_coop = 0
n_def = 0
test = 0

np.set_printoptions(precision=3, suppress=True)


def to_index(a):
    return a.dot(1 << np.arange(a.size)[::-1])


def strategy(history: np.ndarray, memory):
    global predictions, N, last_prediction, correct, naughtiness, n_coop, n_def, test

    # initialize
    if memory is None:
        predictions = 0
        correct = 0
        naughtiness = 0.05
        n_coop = 0
        n_def = 0
        test = 0
        last_prediction = 0
        memory = np.zeros((2, 2 ** N))
        # Probability
        memory[0] = 0.5
        # Weight
        memory[1] = 1.0

    turn = history.shape[1]
    if turn > 0:
        n_coop += history[1, -1]
        n_def += 1 - history[1, -1]

    if turn > N + 1:
        last_play = history[0, -1]
        if turn == N + 2:
            if n_def <= 1:
                naughtiness = -1

        if last_prediction == history[1, -1]:
            correct += 1

        # Increase chance to randomly cheat
        if history[1, -1] == 1 and last_play == 1:
            naughtiness += 0.01
        else:
            naughtiness = max(0.01, naughtiness - 0.005)

        recent = history[1, -N - 1 : -1]

        # Treat recent N plays as a bit string and index into the memory array
        indx = to_index(recent)

        # Average them
        w = memory[1, indx]
        memory[0, indx] = memory[0, indx] * (1 - w) + history[1, -1] * w

        # update weight
        memory[1, indx] *= LEARN_RATE

        # Get probability and make prediction
        prob = memory[0, to_index(history[1, -N:])]
        if test == -2:
            prob *= 2
        if prob > MIN_CONFIDENCE:
            pred = 1
        else:
            pred = 0
        last_prediction = pred

        if test == 1:
            # We're testing to see if this player is titfortat-like
            if history[1, -1] == 0:
                # Probably
                naughtiness = -5
                test = -2
                play = 1
            else:
                # No
                test = -1
                play = pred
        else:
            if test == 3:
                test = 1

            # Make a play decision based on prediction
            play = pred
            # Act naughty sometimes
            if last_play == 1 and pred == 1 and np.random.random() < naughtiness:
                play = 0
            if (
                test == 0
                and history[0, -2] == 1
                and last_play == 1
                and np.random.random() < prob
            ):
                play = 0

            # Initiate t4t test
            if play == 0 and test == 0:
                test = 3

        predictions += 1
    else:
        if turn == 2 and n_def > 0:
            play = 0
        else:
            play = 1
    return play, memory
