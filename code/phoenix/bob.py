
def strategy(history, memory):
    choice = 1
    R = 0.5

    world = memory

    if world is None:
        world = 1

    if history.shape[1] >= 5 and history[1, -5:].sum() > 0:
        world += R * (1 - world)
    else:
        world += R * (0 - world)

    if world < 0.5:
        choice = 0

    return choice, world
