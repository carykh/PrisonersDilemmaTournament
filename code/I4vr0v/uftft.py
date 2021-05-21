# Ultra-forgiving Tit for Tat.
# Defect iff last 3 turns were defections.
def strategy(history, memory):
    choice = 1
    if (
        history.shape[1] >= 3
        and history[1, -1] == 0
        and history[1, -2] == 0
        and history[1, -3] == 0
    ):
        choice = 0
    return choice, None
