# Reminder: For the history array, "cooperate" = 1, "defect" = 0

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
    if round <=16:
        return False
    randomness = 0
    for i in range (1, 10):
        if history[1,-i] == 0:
            if history[0,-i-1] and history[0,-i-2] and history[0,-i-3]:
                randomness+=1
    if randomness>=2:
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
    if round<=10:
        return "defect", memory
    sum = 0
    for i in range (1, 11):
        sum += 1-history[1, -i]
    if sum ==10:
        memory[TACTIC] = "absolution"
        memory[COOLDOWN] = 3
        memory[TOTALLYISNTRANDOM] = True
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
    return forgivingCopycat(history), memory



def strategy(history, memory):
    round = history.shape[1]
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
    if detectSwitch(history):
        if memory[TOTALLYISNTSWITCH]:
            memory[TACTIC] = "goWithSwitch"
        else:
            memory[TACTIC] = "abuseSwitch"
    if memory[TOTALLYISNTRANDOM] == 0 and detectRandomness(history):
        memory[TACTIC] = "abuseRandomness"
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
    print(memory[TACTIC])
    return "cooperate", memory
