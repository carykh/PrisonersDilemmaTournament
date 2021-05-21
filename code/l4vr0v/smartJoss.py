import random

# Variant of Tit For Tat that randomly defects to try to take advantage
# of overly forgiving opponents. But we break out of Tit for Tat if we realize
# they're just responding to our defection.


def strategy(history, memory):
    opponents_last_move = history[1, -1] if history.shape[1] >= 1 else 1
    our_second_last_move = history[0, -2] if history.shape[1] >= 2 else 1
    # only forgive defections if they've cooperated with us before
    choice = (
        1
        if (opponents_last_move == 1 or (memory is True and our_second_last_move == 0))
        else 0
    )

    memory = (
        True
        if (history.shape[1] > 0 and opponents_last_move == 1 or memory is True)
        else False
    )
    if random.random() < 0.10:
        choice = 0

    return choice, memory
