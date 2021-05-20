# Forgiving Tit for Tat.
# Choose to defect if and only if the opponent just defected TWICE in a row.
def strategy(history, memory):
    choice = 1
    if (
        history.shape[1] >= 2 and history[1, -1] == 0 and history[1, -2] == 0
    ):  # We check the TWO most recent turns to see if BOTH were defections, and only then do we defect too.
        choice = 0
    return choice, None
