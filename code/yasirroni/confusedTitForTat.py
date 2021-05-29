def strategy(history, memory):
    choice = 1
    if (
        history.shape[1] >= 1 and history[1, -1] == 1
    ):  # Choose to defect if and only if the opponent just cooperate.
        choice = 0
    return choice, None
