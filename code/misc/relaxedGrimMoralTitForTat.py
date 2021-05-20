def strategy(history, memory):
    """
    Grim Moral Tit For Tat, except we punish them 5 times in a row before giving them
    another chance.
    memory: (inPunishMode, counter)
    """

    if memory is not None and memory[0] is True:
        remainingPunishments = memory[1] - 1
        punishMode = remainingPunishments > 0
        return 0, (punishMode, remainingPunishments)

    if memory is not None and memory[1] >= 5:
        return 0, (True, 4)

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
        memory = (False, 1) if memory is None else (False, memory[1] + 1)

    return choice, memory
