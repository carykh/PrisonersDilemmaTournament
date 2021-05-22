def strategy(history, memory):
    if memory is None or 1 == memory:
        return 0, 0
    else:
        return 1, 1
