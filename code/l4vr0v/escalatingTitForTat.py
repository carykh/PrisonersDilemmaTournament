def strategy(history, memory):
    """
    Tit-for-tat, except we punish them N times in a row if this is the Nth time they've
    initiated a defection.

    memory: (initiatedDefections, remainingPunitiveDefections)
    """
    if memory is not None and memory[1] > 0:
        choice = 0
        memory = (memory[0], memory[1] - 1)
        return choice, memory

    num_rounds = history.shape[1]
    opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
    our_last_move = history[0, -1] if num_rounds >= 1 else 1
    our_second_last_move = history[0, -2] if num_rounds >= 2 else 1

    opponent_initiated_defection = (
        opponents_last_move == 0 and our_last_move == 1 and our_second_last_move == 1
    )
    choice = 0 if opponent_initiated_defection else 1
    if choice == 0:
        memory = (1, 0) if memory is None else (memory[0] + 1, memory[0])

    return choice, memory
