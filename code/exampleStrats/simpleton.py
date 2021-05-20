# Strategy described in Nicky Case's "The Evolution of Trust"
# https://ncase.me/trust/
#
# SIMPLETON: Hi! I try to start by cooperating. If  you cooperate
# back, I do the same thing as my last move, even if it was a mistake.
# If you cheat back, I do the opposite thing as my last move, even
# if it was a mistake.


def strategy(history, memory):
    choice = None
    if history.shape[1] == 0:  # We're on the first turn!
        choice = 1
    else:
        choice = history[0, -1]  # I will keep doing the same thing as last move!
        if (
            history[1, -1] == 0
        ):  # If my opponent defected last turn, I'll just do the opposite thing as my last move:
            choice = 1 - choice

    return choice, None
