import numpy as np
import random

n = 10
seq = 1
# f = open("./logs.txt", "a+")
def repeat(s):
    i = (s + s).find(s, 1, -1)
    return None if i == -1 else s[:i]


def strategy(history, memory):
    global seq  # , f
    """
    Defect every n turns
    """
    if memory == None:
        memory = 0.1
    choice = int((history.shape[1] + 1) % n != 0)
    lastx = history[1, -seq:]
    if history.shape[1] > 2:
        if np.all(lastx == 1):
            choice = 1
        if np.all(lastx == 0):
            choice = 0

    past = (history[1, -6:] - 0.5) * 2
    if len(past) > 3:
        strPast = "".join(["1" if x == 1 else "0" for x in past])
        r = repeat(strPast)
        if r == "10" or r == "01":
            choice = 0
    if choice == 0 and list(history[1]).count(0) < 5:
        choice = 1
        # f.write(f"{strPast}, {r}\n")
    return choice, memory
