# Tit for tat, but averages history instead of just copying whatever was last.
# Just like normal TFT, cooperates on first round
#
# Created by Aquateraneal

def strategy(history, memory):
    choice = 1
    if history.shape[1]:
        choice = round(sum(history[1])/len(history[1]))
    return choice, None
