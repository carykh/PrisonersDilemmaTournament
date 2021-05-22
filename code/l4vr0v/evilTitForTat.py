def strategy(history, memory):
    """
    If opponent defected out of the blue, respond with defection.
    Begin game with defection for first two rounds.
    """
    num_rounds = history.shape[1]
    if num_rounds < 2:
        return 0, None

    opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
    opponents_second_last_move = history[1, -2] if num_rounds >= 2 else 1
    our_second_last_move = history[0, -2] if num_rounds >= 2 else 1
    choice = (
        1
        if (
            opponents_last_move == 1
            or (our_second_last_move == 0 and opponents_second_last_move == 1)
        )
        else 0
    )
    return choice, None
