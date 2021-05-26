def strategy(history, memory):
    choice = 1

    if memory is None:
        memory = [0]

    responsiveness = memory[0]

    if history.shape[1] >= 1:
        # "responsiveness check" suggested by valadaptive
        if history.shape[1] >= 4:
            # I defect; you defect (good)
            if history[0, -2] == 0 and history[1, -2] == 0:
                responsiveness += 2
            # I coop; you coop (good)
            elif history[0, -2] == 1 and history[1, -1] == 1:
                responsiveness += 1
            # I defect; you coop (sus)
            elif history[0, -2] == 0 and history[1, -1] == 1:
                # they might be forgiving so don't be as punishing
                if history[0, -3] == 0:
                    responsiveness -= 2
                else:
                    responsiveness -= 1
            # I coop; you defect (sus)
            elif history[0, -2] == 1 and history[0, -1] == 0:
                # TODO: they may be a joss so don't be too punishing
                responsiveness -= 1

        if responsiveness < 0:
            choice = 0
        else:
            choice = history[1, -1]

    return choice, [responsiveness]
