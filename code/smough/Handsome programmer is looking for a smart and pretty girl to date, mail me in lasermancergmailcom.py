# Reminder: For the history array, "cooperate" = 1, "defect" = 0
import random

def forgivingCopycat(history):
    round = history.shape[1]
    if history[1,-1] == 0:
        if round > 3:
            if history [0, -1] == 1 and history [0,-2] == 0 and history [1, -2] == 1:
                return "cooperate"
        return "defect"
    return "cooperate"

def detectRandomness(history):
    round = history.shape[1]
    if round <=41:
        return False
    randomness = 0
    for i in range (1, 41):
        if history[1,-i] == 0:
            if history[0,-i-1]:
                randomness+=1
    if randomness>=16:
        print("randomness detected")
        return True
    return False

def detectSwitch(history):
    round = history.shape[1]
    if round <=10:
        return False
    if history[1,-1] and history[1, -2] ==0 and history[1,-3] and history[1, -4] ==0 and history[1,-5] and history[1, -6] ==0:
        return True
    if history[1,-1]==0 and history[1, -2] and history[1,-3] ==0 and history[1, -4] and history[1,-5] ==0and history[1, -6]:
        return True
    return False

def tryRandomness(history, memory):
    round = history.shape[1]
    TACTIC = 2
    COOLDOWN = 3
    TOTALLYISNTRANDOM = 5
    sum = 0
    for i in range (1, 6):
        sum += 1-history[1, -i]
    if sum ==10:
        memory[TACTIC] = "absoluteMe"
        memory[COOLDOWN] = 3
        memory[TOTALLYISNTRANDOM] = True
        print("Not Randomness")
        return "cooperate", memory
    return "defect", memory

def absoluteMe(history, memory):
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED = 4
    if memory[COOLDOWN] >0:
        memory [COOLDOWN] -=1
        return "cooperate", memory
    sum = history [1, -1] + history [1, -2] + history [1, -3]
    if sum >=1:
        memory[TACTIC] = "abuseCopykitten"
        memory[COOLDOWN] = 0
        return "cooperate", memory
    memory[TACTIC] = "reallyuntruthworthy"
    return "defect", memory 

def abuseCopykitten(history, memory,delay):
    round = history.shape[1]
    TACTIC = 2
    if round >= delay+18:
        sin = 0
        for i in range (1, 13):
            if history[1, -i] == 0:
                sin+=1
        if sin>=4:
            memory[TACTIC] = "priest"
            return "cooperate", memory
    sin = 0
    if round <= delay+12:
        for i in range (1, 7):
            if history[1, -i] == 0:
                sin+=1
        if sin>=3:
            memory[TACTIC] = "priest"
            return "cooperate", memory
    if round%6 == 0:
         return "cooperate", memory
    if round%6 == 1:
         return "cooperate", memory
    if round%6 == 2:
         return "cooperate", memory
    if round%6 == 3:
         return "defect", memory
    if round%6 == 4:
         return "cooperate", memory
    if round%6 == 5:
         return "defect", memory

def abuseSwitch(history, memory):
    round = history.shape[1]
    ABSOLUTION = 0
    LASTABSOLUTION = 1
    TACTIC = 2
    COOLDOWN = 3
    TOTALLYISNTSWITCH = 6
    if history[1,-1]==0 and history[1, -2] ==0 and history[1,-3] ==0 and history[1, -4]==0:
        memory[TACTIC] = "absolution"
        memory[LASTABSOLUTION] = round
        memory[COOLDOWN] = 3
        memory[TOTALLYISNTSWITCH] = True
        return "cooperate", memory
    return "defect", memory

def goWithSwitch(history, memory):
    round = history.shape[1]
    ABSOLUTION = 0
    LASTABSOLUTION = 1
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED= 4
    TOTALLYISNTSWITCH = 6
    if history[1,-1]==0 and history[1, -2] ==0 and history[1,-3] ==0 and history[1, -4]==0:
            sum = 0
            for i in range (1, round-memory[LASTABSOLUTION]+1):
                if history[1,-i]:
                    if history[0, -i]:
                        sum+=2
                    else:
                        sum+=4
                else:
                    if history[0,-i]:
                        sum-=1
                    else:
                        sum+=0
            if sum <= 0:
                memory[TACTIC] = "untruthworthy"
                memory[UNTRUTHWORTHIED]+=1
            else:
                memory[LASTABSOLUTION] = round
                memory[TACTIC] = "absolution"
                memory[ABSOLUTION] = False
    if history[1, -1]:
        return "defect", memory
    return "cooperate", memory

def abuseRandomness(history, memory):
    round = history.shape[1]
    TACTIC = 2
    COOLDOWN = 3
    TOTALLYISNTRANDOM = 5
    if round<=12:
        return "defect", memory
    sum = 0
    for i in range (1, 13):
        sum += 1-history[1, -i]
    if sum ==12:
        memory[TACTIC] = "absolution"
        memory[COOLDOWN] = 3
        memory[TOTALLYISNTRANDOM] = True
        return "cooperate", memory
    return "defect", memory

def abuseForgivingcopycat(history, memory, delay):
    round = history.shape[1]
    LASTABSOLUTION = 1
    TACTIC = 2
    if history[1,-1]==0 and round != delay+6:
        memory[TACTIC] = "abuseCopykitten"
        return "cooperate", memory
    if history[0,-1]:
        return "defect", memory
    return "cooperate", memory

def abuseAlwayscooperate(history, memory):
    TACTIC = 2
    COOLDOWN = 3
    if history[1,-1]==0 and history[1,-2] == 0:
        memory[TACTIC] = "absolution"
        memory[COOLDOWN] = 3
        return "cooperate", memory
    return "defect", memory

def untruthworthy(history, memory):
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED = 4
    if memory[UNTRUTHWORTHIED] >=3:
        memory[TACTIC]= "reallyuntruthworthy"
        memory[COOLDOWN] = 0
    if history [1, -1] == 1 and history [1, -2] == 1:
        memory[COOLDOWN] = 0
        memory[TACTIC]= "priest"
        return "cooperate", memory

    return "defect", memory

def reallyuntruthworthy(history, memory):
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED = 4
    memory[COOLDOWN]+=1
    if history [1, -1] == 1 and history [1, -2] == 1 and history [1, -3] == 1 :
        memory[TACTIC]= "priest"
        memory[COOLDOWN] = 0
        return "cooperate", memory
    if memory[COOLDOWN] >=8 and memory[UNTRUTHWORTHIED] >=3:
        memory[TACTIC]= "untruthworthy"
        memory[UNTRUTHWORTHIED]= -200
    return "defect", memory

def absolution(history, memory):
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED = 4
    if memory[COOLDOWN] >0:
        memory [COOLDOWN] -=1
        return "cooperate", memory
    sum = history [1, -1] + history [1, -2] + history [1, -3]
    if sum >=1:
        memory[TACTIC] = "priest"
        memory[COOLDOWN] = 0
        return "cooperate", memory
    memory[TACTIC] = "reallyuntruthworthy"
    return "defect", memory 

def priest(history, memory):
    round = history.shape[1]
    ABSOLUTION = 0
    LASTABSOLUTION = 1
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED = 4
    memory[COOLDOWN] +=1
    if history [1, -1]== 0 and history [1, -2]== 0 and history [1, -3]== 0:
        if memory[ABSOLUTION]:
            memory[LASTABSOLUTION] = round
            memory[TACTIC] = "absolution"
            memory[ABSOLUTION] = False
            memory[COOLDOWN] = 3
        else:
            sum = 0
            for i in range (1, round-memory[LASTABSOLUTION]+1):
                if history[1,-i]:
                    if history[0, -i]:
                        sum+=2
                    else:
                        sum+=4
                else:
                    if history[0,-i]:
                        sum-=1
                    else:
                        sum+=0
            if sum <= 0:
                memory[TACTIC] = "untruthworthy"
                memory[UNTRUTHWORTHIED]+=1
            else:
                memory[LASTABSOLUTION] = round
                memory[TACTIC] = "absolution"
                memory[ABSOLUTION] = False
    if history[1,-1] ==0:
        sin = 0
        for i in range (1,11):
            if history[1, -i] ==0 and history[0,-i-1]:
                sin+=1
        if sin <=random.randint(1,10) and sin-1 <=random.randint(1,10):
            return "cooperate", memory
    return forgivingCopycat(history), memory



def strategy(history, memory):
    round = history.shape[1]
    delay = 17
    ABSOLUTION = 0
    LASTABSOLUTION = 1
    TACTIC = 2
    COOLDOWN = 3
    UNTRUTHWORTHIED = 4
    TOTALLYISNTRANDOM = 5
    TOTALLYISNTSWITCH = 6
    if round == 0:
            mem = []
            mem.append(True)
            mem.append(True)
            mem.append(0)
            mem.append(0)
            mem.append(0)
            mem.append(False)
            mem.append(False)
            return "cooperate", mem
    if round == 1:
        return "cooperate", memory
    if round == 2:
        return "cooperate", memory
    if round == 3:
        memory[TACTIC] = "priest"
        if history[1, -1] ==0 or history[1, -2] ==0 or history[1, -3] ==0:
            if history[1, -1] ==0 and history[1, -2] ==0 and history[1, -3] ==0:
                memory[ABSOLUTION] = False
            return "defect", memory
        else:
            return "cooperate", memory
    if 4<=round<=delay:
        return forgivingCopycat(history), memory
    if round == delay+1:
        sin = 0
        for i in range (1, 9):
            sin+=1-history[1,-i]
        if sin >=7:
            memory[TACTIC] = "untruthworthy"
            return "defect", memory
        return "cooperate", memory
    if memory[TACTIC] == "untruthworthy":
        return untruthworthy(history, memory)
    if round == delay+2:
        return "cooperate", memory
    if round == delay+3:
        return "defect", memory
    if round == delay+4:
        return "defect", memory
    if round == delay+5:
        return "cooperate", memory
    if round == delay+6:
        sin = 0
        for i in range (1, 5):
            sin+=1-history[1,-i]
        if history[1,-1] == 0 and history[1,-2]and history[1,-3]:
            memory[TACTIC] = "abuseForgivingcopycat"
        elif history[1,-1] and history[1,-2] and history[1,-3] and history[1,-4] and history[1,-5] and history[1,-6]:
            memory[TACTIC] = "abuseAlwayscooperate"
        elif history[1,-1] ==0 and history[1,-2]==0 and history[1,-3] and (history[1,-4] or history[0,-5]==0):
            memory[TACTIC] = "abuseCopykitten"
        else:
            memory[TACTIC] = "tryRandomness"
    if detectSwitch(history) and memory[TACTIC] != "abuseRandomness" and memory[TACTIC] != "tryRandomness":
        if memory[TOTALLYISNTSWITCH]:
            memory[TACTIC] = "goWithSwitch"
        else:
            memory[TACTIC] = "abuseSwitch"
    if memory[TOTALLYISNTRANDOM] == 0 and detectRandomness(history):
        memory[TACTIC] = "abuseRandomness"
    if memory[TACTIC] == "tryRandomness":
        if round >=delay+6+10:
            memory[TACTIC] = "abuseRandomness"
        else:
            return tryRandomness(history, memory)
    if memory[TACTIC] == "absoluteMe":
        return absoluteMe(history, memory)
    if memory[TACTIC] == "priest":
        return priest(history, memory)
    if memory[TACTIC] == "abuseSwitch":
        return abuseSwitch(history, memory)
    if memory[TACTIC] == "goWithSwitch":
        return goWithSwitch(history, memory)
    if memory[TACTIC] == "absolution":
        return absolution(history, memory)
    if memory[TACTIC] == "abuseRandomness":
        return abuseRandomness(history, memory)
    if memory[TACTIC] == "untruthworthy":
        return untruthworthy(history, memory)
    if memory[TACTIC] == "reallyuntruthworthy":
        return reallyuntruthworthy(history, memory)
    if memory[TACTIC] == "abuseCopykitten":
        return abuseCopykitten(history, memory, delay)
    if memory[TACTIC] == "abuseForgivingcopycat":
        return abuseForgivingcopycat(history, memory,delay)
    if memory[TACTIC] == "abuseAlwayscooperate":
        return abuseAlwayscooperate(history, memory)
    print(memory[TACTIC])
    return "cooperate", memory
