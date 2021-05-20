import numpy

def strategy(history, memory):
    choice = 1
    if history.shape[1] != 0:
        percents = numpy.mean(history, axis=1)
        if percents[0] > percents[1] + 0.1:
            choice = 0
    return choice, None