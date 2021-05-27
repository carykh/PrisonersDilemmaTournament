import random

def getChoice(snitch):
    return "tell truth" if snitch else "stay silent"

def strategy(history, memory):
    snitch = random.random() < 0.20
    return getChoice(snitch), None
