#a super very mega angery version of n3ptune, im angery! $%&!
#by usedToBeTomas

import random

def strategy(history, memory):
    #memory init
    if memory == None:
        memory = [False,True,"",False,[0,0,0,0,0]]
    interval = memory[0]
    flip = memory[1]
    string_history = memory[2]
    is_pattern = memory[3]
    random_m = memory[4]

    #n3ptune base algo but different...idk
    choice = 1
    if history.shape[1] >= 1 and history[1, -1] == 0:
        choice = 0
        if history.shape[1] % 15 < 2:
            choice = 1
        if history.shape[1] % 15 == 1 and interval:
            choice = 0
            interval = False
        elif history.shape[1] % 15 == 1:interval = True

    #flip attack
    if flip and history.shape[1] >= 8 and not(sum(history[1])==history.shape[1]):
        if history.shape[1]%2==0:
            choice = 0
        else:
            choice = 1
            if sum(history[1])==history.shape[1]-1 and sum(history[0])==history.shape[1]:
                choice = 0
            if history[1][-1] == 0 and history[1][-2] == history[1][-3] == history[1][-4] == history[1][-5] == 1:
                if history[1][-6] == history[1][-7] == history[1][-8] == history[1][-9] == 1:
                    if history[0][-1] == 1 and history[0][-2] == 0 and history[0][-3] == 1 and history[0][-4] == 0 and history[0][-5] == 1:
                        if history[0][-6] == 0 and history[0][-7] == 1 and history[0][-8] == 0 and history[0][-9] == 1:
                            is_pattern = True
                    if history[0][-1] == 0 and history[0][-2] == 1 and history[0][-3] == 0 and history[0][-4] == 1 and history[0][-5] == 0:
                        if history[0][-6] == 1 and history[0][-7] == 0 and history[0][-8] == 1 and history[0][-9] == 0:
                            is_pattern = True
        if history[1, -1] == history[1, -3] == 0 and history[1, -2] == history[1, -4] == 1:
            flip = False
        if history[1, -1] == history[1, -2] == history[1, -3] == 0:
            flip = False
        if history.shape[1] >= 28 and (sum(history[1])*2)<history.shape[1]:
            flip = False
        if not(flip):
            choice = 1
            


    #anti random
    memory3 = random_m
    if history.shape[1]>1 and history[1, -1] == 0 and history[0, -2] == 1:
        memory3[0]+=1
    if history.shape[1]>1 and history[0, -2] == 0 and history[1, -1] == 1:
        memory3[1]+=1
    if history.shape[1]==40:
        xxx = (sum(history[1])*2)/history.shape[1]
        if history.shape[1]==40 and memory3[0]>6 and memory3[1]>4 and memory3[0]!=memory3[1] and xxx>0.75 and xxx<1.25:
            if not(history[1, 0] == 1 and history[1, 1] == 1 and history[1, 2] == 0 and history[1, 3] == 1 and history[1, 4] == 0 and history[1, 5] == 1):
                memory3[2] = 1
    if history.shape[1]==60:
        xxx = (sum(history[1])*2)/history.shape[1]
        if history.shape[1]==60 and memory3[0]>8 and memory3[1]>6 and memory3[0]!=memory3[1] and xxx>0.9 and xxx<1.1:
            if not(history[1, 0] == 1 and history[1, 1] == 1 and history[1, 2] == 0 and history[1, 3] == 1 and history[1, 4] == 0 and history[1, 5] == 1):
                memory3[2] = 1
    if memory3[2] == 1 and history.shape[1]>40:
        choice = 0
    #inverted mirrors exploit
    if memory3[1]==4 and memory3[3] == 0:
        if history[0, -1] == 0 and history[1, -1] == 1 and history[0, -2] == 0 and history[1, -2] == 0 and history[1, 0] == 0:
            memory3[3] = 1
    if memory3[3] == 1 and history[1, -1] == 0:
        memory3[3] = 2
    if memory3[3] == 1:
        choice = 0
    random_m = memory3

    
    #anti always defect
    if sum(history[1]) <=3 and history.shape[1] > 25:
        choice = 0
        
    #anti pattern
    if history.shape[1] >=1:
        string_history+=str(history[1,-1])
    patterns = ["1010101010101010","0101010101010101","1100110011001100110011001100","0100110011001100110011001100",
                "001100110011001100110011001100","11011011011011011011011011","011011011011011011011011","1001001001001001001001001"
                ,"1011011011011011011011011011","0001000100010001000100010001000"]
    if history.shape[1]<=40 and history.shape[1]>10:
        found = False
        for i in patterns:
            if string_history == i:
                found = True
        if found:
            is_pattern = True
    if is_pattern:
        choice = 0
        
    
        
    
    memory = [interval,flip,string_history,is_pattern,random_m]
    return choice, memory
