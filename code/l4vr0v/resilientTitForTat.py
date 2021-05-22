def strategy(history, memory):
    """
    Tit for Tat, but it only defects once in a row.
    """
    choice = 1
    if (
        history.shape[1] >= 1
        and history[1, -1] == 0
        and memory is not None
        and 1 == memory
    ):
        choice = 0
    return choice, choice
