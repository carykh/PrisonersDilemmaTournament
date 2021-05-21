def strategy(history, memory):
    """
    Tit for Tat, but it only defects once in a row unless its opponent defected twice
    in a row.
    """
    choice = 1
    num_rounds = history.shape[1]
    opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
    opponents_second_last_move = history[1, -2] if num_rounds >= 2 else 1
    my_last_move = history[0, -1] if num_rounds >= 1 else 1

    if opponents_last_move == 0:
        if my_last_move == 0:
            choice = opponents_second_last_move
        else:
            choice = 0
    return choice, None
