# We will cooperate repeatedly until our opponent betrays us twice.
# Then, we will get angry and defect for the rest of time.


def strategy(history, wrongedCount):
    if wrongedCount is None:
        wrongedCount = 0
    if history.shape[1] >= 1 and history[1, -1] == 0:  # Just got wronged.
        wrongedCount += 1

    choice = 0 if wrongedCount >= 2 else 1

    return choice, wrongedCount
