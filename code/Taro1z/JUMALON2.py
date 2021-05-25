#ARVINJAY JUMALON.
#Input List:
#Memory: The criteria for defining the "character" of the opponent. [Wronged List, Successful Cooperations, Sudden Betrayals, Current Character Ranking, Successful Exploits]

import numpy as np

def titfortat(memory): #Characters that are trustworthy should be cooperated with
    memory[6] = 0
    choice = "cooperate"
    if history[1,-1] == 0:
        choice = "defect"
def investigate(memory): #Characters that have the potential to be a good ally, but keep themselves mysterious, should be investigated
    if memory[6] = 0:
        memory[6] = memory[2]
        flag = memory[6]
    choice = "defect"
    if history[1,-1] == 1 or history[0,-1] == 0: #Never defect twice in a row
        choice = "cooperate"
    memory[6] += 1
    if memory[6] == flag + 3 and memory[6] - flag > memory[2] - flag + 2: #If there were less than two successful cooperations within 4 moves
        choice = history[1,-1]
    elif memory[6] == flag + 3:
        flag = memory[6]
        memory[6] = 0
        choice = "cooperate"
    
def ignore(): #Characters that have betrayed too many times should be ignored to cut losses
    memory[6] = 0
    choice = "defect"
def exploit(memory): #Characters that are too trusting should be exploited
    memory[6] = 0
    choice = "cooperate"
    if history [0,-1] = 1:
        choice = "defect"
def ftft(memory): #Characters that have proved themselves to be very trustworthy should be forgiven sometimes
    memory[6] = 0
    choice = "cooperate"

    if history[1,-1]+history[1,-2] == 0:
        choice = "defect"

def assess(memory): #The process used to access the opponents character

    if history[1,-1] == 0: #wronged counter
        memory[1] += 1
    if history[1,-1] == 1 and history[0,-1] == 1: #successful cooperations counter
        memory[2] += 1
    if memory[4] == "exploitable" and history[1,-1] == 1 and history[0,-1] == 0: #successful exploits counter
        memory[5] += 1
        
    num_rounds = history.shape[1]
    
    if num_rounds < 8:
        memory[4] = "unknown"
    elif num_rounds < 25:
        if memory[1] > memory[2]:
            memory[4] = "untrustworthy"
        elif num_rounds/2 >= memory[2]:
            memory[4] = "trusted"
        else memory[4] = "unknown"
    elif num_rounds < 100:
        if memory[1] > memory[2]:
            memory[4] = "untrustworthy"
        elif memory[4] == "trusted" and memory[1] < num_rounds/4
            memory[4] == "supertrusted"
        elif memory[2] >= .9 * num_rounds: #Constant 1: Exploit search 
            memory[4] == "exploitable"
        else memory[4] == "unknown"
    elif num_rounds < 170:
        if memory[1] > memory[2]:
            memory[4] = "untrustworthy"
        elif memory[4] == "trusted" and memory[1] < num_rounds/4:
            memory[4] == "supertrusted"
        elif num_rounds/2 >= memory[2] and memory[1] < num_rounds/3:
            memory[4] = "trusted"
        elif memory[2] >= .8 * num_rounds: #constant 2
            memory[4] == "exploitable"
        else memory[4] == "unknown"
    else:
        if memory[1] > memory[2]:
            memory[4] = "untrustworthy"
        elif memory[4] == "trusted" and memory[1] < num_rounds/4
            memory[4] == "supertrusted"
        elif num_rounds/2 >= memory[2] and memory[1] < num_rounds/3:
            memory[4] = "trusted"
        elif memory[2] >= .7 * num_rounds: #constant 3
            memory[4] == "exploitable"
        else memory[4] = "unknown"

    if history[1,-1] == 0 and history[1,-2]*history[1,-3]*history[1,-4] == 1: #sudden betrayal counter
        memory[3] += 1
        memory[4] == "unknown"

def stratagy(history, memory):
    if num_rounds = 0:
        memory = [0 0 0 "unknown" 0 0]
        choice = "cooperate"
    elif memory[4] == "unknown":
        choice = investigate(history)
        memory[4] = assess(memory)
    elif memory[4] == "untrustworthy":
        choice = ignore()
        memory[4] = assess(memory)
    elif memory[4] == "exploitable":
        choice = exploit(history)
        memory[4] = assess(memory)
    elif memory[4] == "trusted":
        choice = titfortat(history)
        memory[4] = assess(memory)
    elif memory[4] == "supertrusted":
        choice = ftft(history)
        memory[4] = assess(memory)
    return choice,memory
        
