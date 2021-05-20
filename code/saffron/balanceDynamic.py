import numpy

def strategy(history, memory):
    choice = 1
    if history.shape[1] != 0:
        percents = numpy.average(history, axis=1, weights=memory[::-1])
        if percents[0] > percents[1] + 0.1:
            choice = 0
        memory.append(0.85 ** len(history))
    else:
        memory = [1]
    return choice, memory