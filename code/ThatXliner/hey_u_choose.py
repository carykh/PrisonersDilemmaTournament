def strategy(history, memory):
    US = history[0]
    THEM = history[1]
    gametime = history.shape[1]
    they_bad = len(list(filter(lambda x: x == 0, THEM)))
    they_good = len(list(filter(lambda x: x == 1, THEM)))
    if gametime == 0:  # Go coop first
        return "stay silent", None
    if they_good > they_bad:
        return "stay silent", None
    else:
        return "tell truth", None
