import random as r

strats = ["GrumpyTitForTat","GrimTrigger","RNG","ForgivingTitForTat","Simpleton","AlwaysCooperate","AlwaysDefect"]

def GrumpyTitForTat(history, memory): #It's another Tit for Tat variant! Yay!
    choice = 1
    if len(history[0]) > 1:
        choice = history[1,-1] #Standard Tit for Tat stuff.
        courage = 0 #Oh? What is this??
        for x in range(len(history[0])):
            courage += 2 * history[1, x] - 1 #If the opponent defects, 1 is subtracted, and if the opponent cooperated, 1 is added.
        courage /= len(history[0])  #"Courage" is a simple way to see if the opponent is defecting too much. If it is, this value should be nagative, and if it's about the same it should be near 0, etc.
        if courage < 0 and len(history[0]) > 3: #If it defects a bit too much(the .01 is for detecting random or alternating strategies as well as the strategies which defect more than they cooperate), start defecting.
            choice = 0
    return choice, None

def GrimTrigger(history, memory):
    return 1 - (0 in history[1]), None

def RNG(history, memory):
    return r.randint(0,1), None

def ForgivingTitForTat(history, memory):
    choice = 1
    if (history.shape[1] >= 2 and history[1, -1] + history[1, -2] == 0):
        choice = 0
    return choice, None

def Simpleton(history, memory):
    choice = None
    if history.shape[1] == 0:  # We're on the first turn!
        choice = 1
    else:
        choice = history[0, -1]  # I will keep doing the same thing as last move!
        if (history[1, -1] == 0):  # If my opponent defected last turn, I'll just do the opposite thing as my last move:
            choice = 1 - choice
    return choice, None

def AlwaysCooperate(history, memory):
    return 1, None

def AlwaysDefect(history, memory):
    return 0, None

def strategy(history, memory):
    params = [2.2528726547063944, 0.257890650655991, -0.05331344719399757, 0.25704264781322955, -0.6356013750816252, 0.7286967962439984, 0.7564962826327676]
    choice = 1
    hi = 0
    crap1, crap2 = GrumpyTitForTat(history, memory)
    hi += params[0] * (2 * crap1 - 1)
    crap1, crap2 = GrimTrigger(history, memory)
    hi += params[1] * (2 * crap1 - 1)
    crap1, crap2 = RNG(history, memory)
    hi += params[2] * (2 * crap1 - 1)
    crap1, crap2 = ForgivingTitForTat(history, memory)
    hi += params[3] * (2 * crap1 - 1)
    crap1, crap2 = Simpleton(history, memory)
    hi += params[4] * (2 * crap1 - 1)
    crap1, crap2 = AlwaysCooperate(history, memory)
    hi += params[5] * (2 * crap1 - 1)
    crap1, crap2 = AlwaysDefect(history, memory)
    hi += params[6] * (2 * crap1 - 1)
    choice = 1 * (hi >= 0)
    return choice, params
