import random

def strategy(history, memory):
    a = 3
    b = 8
    if memory == None:
        return 1, [0,0,0,0,0,0,0,False]
    if not memory[7]: 
        memory[4] += 1
        if history[1,-1] == 1:
            memory[3] += 1
    else:
        memory[6] += 1
        if history[1,-1] == 1:
            memory[5] += 1
        if memory[6] == 10:
            if memory[5] == 0 and memory[3] > 0:
                memory[1] = 0
                memory[7] = False
                memory[2] = 2
    if memory[2] != 0:
        c = 1
        memory[2] -= 1
    elif memory[0] >= a:
        c = 1
        if memory[0] == a:
            memory[0] += 1
        else:
            memory[0] = 0
    else:
        if history.shape[1] >= 2 and history.shape[1] <= 20:
            if history[1,-1] == 1 and history[1,-2] == 1:
                memory[1] -= 1
            if history[1,-1] != history[1,-2]:
                memory[1] += 1
            if history[1,-1] != history[0,-2]:
                memory[1] += 1
        if memory[1] >= b:
            c = 0
            memory[7] = True
        else:
            c = history[1,-1]
            if history.shape[1] >= 2 and history[1,-1] != history[1,-2]:
                memory[0] += 1
            else:
                memory[0] = 0
    if history.shape[1] >= 1 and history[0,-1] == 0 and history[1,-1] == 0 \
       and c == 0 and memory[3] > 0:
        if memory[1] < b and random.random() <= 0.1:
            c = 1
            memory[2] = 1
    return c, memory
