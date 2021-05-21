def strategy(history, memory):
    """
    Defect every few turns, based on the fibonacci sequence.
    i.e., defect turn 2 (1), turn 3 (1), turn 5 (2), turn 8 (3), turn 13 (5)
    """
    if memory is None:
        last_defection_turn = 0
        prev_fibonacci = 1
        current_fibonacci = 1
    else:
        last_defection_turn, prev_fibonacci, current_fibonacci = memory

    if history.shape[1] == last_defection_turn + current_fibonacci:
        last_defection_turn = history.shape[1]
        next_fibonacci = prev_fibonacci + current_fibonacci
        prev_fibonacci = current_fibonacci
        current_fibonacci = next_fibonacci
        choice = 0
    else:
        choice = 1

    return choice, (last_defection_turn, prev_fibonacci, current_fibonacci)
