def strategy(history, memory):
    """
    If opponent unexpectedly defected more than 5 times, always punish them.
    Otherwise, moral tit for tat.
    """
    if memory is not None and memory >= 5:
        return 0, memory

    num_rounds = history.shape[1]
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
    if choice == 0:
        memory = 1 if memory is None else memory + 1

    return choice, memory
