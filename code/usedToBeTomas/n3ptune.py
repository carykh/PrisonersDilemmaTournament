#n3ptune (tune on 3 points)
#by usedToBeTomas
#
#
#The concept is that standard tit4tat cooperates whenever the opponent attempts
#to initiate a cooperation but it never tries to start a collaboration on its
#own (except the beginning), so i just added that and a few other things.
#
#Actual algorithm =
#-tit4tat
#-2 random Silent(coop) with 5.6% chance(why 5.6? trial and error), only if both our and their move were defect or it has a STSTSTSTST pattern
#-anti random (also works for aggressive strategy)
#-anti switcher/flip/idk (STSTSTSTST)
#-anti always defect
#
#code is poorly written...
#bye


import random

def strategy(history, memory):
    #memory 0doubles,1amount,2history,3switcher,4unprovokedD,5random
    if memory == None:
        memory = [0,0,"",0,0,0]

    #tit4tat + 2 random Silent with 5.6% chance, only if both our last moves were defect
    if memory[0] == 1:
        memory[0] = 2
    if history.shape[1] >= 1 and memory[0]!=2:
        memory[2] += str(history[1,-1])
        if history[1,-1] == 0 and history.shape[1]>1:
            if history[0,-2] == 1:
                memory[4]+=1
            if random.random()>0.056:
                choice = 0
            else:
                if history[0,-1] == 0:
                    choice = 1
                    memory[0] = 1
                else:
                    if memory[2].find("1010101010") != -1:
                        choice = 1
                        memory[0] = 1
                    else:
                        choice = 0
        else:
            if history[1,-1] == 1:
                memory[1] += 1
            choice = 1
    else:
        choice = 1
    if memory[0] == 2:
        choice = 1
        memory[0] = 0

    #anti random
    if history.shape[1]<40 and memory[4]>7:
        memory[5] = 1
    if memory[5] == 1:
        choice = 0

    #anti always defect
    if history.shape[1]>45 and memory[1]==0:
        choice = 0

    #anti switchers
    if memory[3] == 1:
        if history[1,-1] == 0 and history.shape[1]%2 == 1:
            choice = 0
        elif history[1,-1] == 1 and history.shape[1]%2 == 0:
            choice = 0
        else:
            memory[3] = 4
    if memory[3] == 2:
        if history[1,-1] == 1 and history.shape[1]%2 == 1:
            choice = 0
        elif history[1,-1] == 0 and history.shape[1]%2 == 0:
            choice = 0
        else:
            memory[3] = 4
    if history.shape[1] == 40:
        if memory[2][-15:] == "101010101010101" and memory[2][:2] != "11" and memory[2][:2] != "00":
            choice = 0
            memory[3] = 1
        elif memory[2][-15:] == "010101010101010" and memory[2][:2] != "11" and memory[2][:2] != "00":
            choice = 0
            memory[3] = 2

    return choice, memory
