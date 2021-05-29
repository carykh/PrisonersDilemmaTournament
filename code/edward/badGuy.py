import random
import numpy as np

DEADLOCK = 3
RANDOM = 7
ABUSEVAL = 2

states = {
    "11,11,": 0,
    "11,10,00,": 0,
    "10,00,01,10,01,":1,
    "11,11,01,10,01,10,":1,
    "11,10,00,00,10,10,":0,

    "01,01,01,01,01,01,":0,
    "01,01,01,01,00,01,":0,
    "01,01,01,00,01,01,":0,
    "01,01,00,01,01,01,":0,
    "01,00,01,01,01,01,":0,
    "00,01,01,01,01,01,":0,
}

def getScore(history,start,end):
    total = 0
    for i in range(start,end):
        if history[0,i] == 1:
            if history[1,i] == 1:
                total += 3
            else:
                total += 0
        elif history[1,i] == 1:
            total += 5
        else:
            total += 1
    return total

def detectRandom(h):
    r = [0,0,0,0]

    swaps = 0

    for i in range(1,h.shape[1]):
        r[2 * h[0, i-1] + h[1, i]] += 1
        if h[1,i] != h[1,i-1]:
            swaps += 1

    if swaps/h.shape[1] < 0.2:
        return False

    s = sum(r)
    a = [
        (r[0] + r[1]) * (r[0] + r[2]) / s,
        (r[1] + r[0]) * (r[1] + r[3]) / s,
        (r[2] + r[3]) * (r[2] + r[0]) / s,
        (r[3] + r[2]) * (r[3] + r[1]) / s,
    ]

    b = [
        (r[0] - a[0]) ** 2 / a[0] if a[0] else 0,
        (r[1] - a[1]) ** 2 / a[1] if a[1] else 0,
        (r[2] - a[2]) ** 2 / a[2] if a[2] else 0,
        (r[3] - a[3]) ** 2 / a[3] if a[3] else 0,
    ]

    x = (sum(b) / 2) ** (1 / 2)

    chance = 1 / (1 + 0.278 * x + 0.231 * x**2 + 0.000973 * x**3 + 0.0781 * x**4) ** 4

    return chance > max(0.02, 0.95 ** h.shape[1]) and 2.7 ** (h[1] == 0).sum() > 5 * h.shape[1]


def strategy(history, memory):
    turns = history.shape[1]
    #first turns; initialize memory
    if turns <= 0:
        return 1, [0,1,0,0,ABUSEVAL,0,0]

    dead = memory[0]
    rand = memory[1]
    abuse = memory[2]
    abused = memory[3]
    abusePeriod = memory[4]
    jossness = memory[5]
    forgave = memory[6]

    deadlock = DEADLOCK

    faults = 0
    for x in range(max(0,turns-10),turns):
        if history[1,x] != history[0,x-1]:
            faults += 1
    if faults > 4:
        jossness = max(0,jossness-100)

    if jossness > 0 and jossness < 3:
        deadlock -= 1
    if jossness > 100:
        deadlock = 0

    #inverted TitForTat detection
    invtft = True
    if turns>5:
        for x in range(1,turns):
            if history[1,-x] == history[0,-x-1]:
                invtft = False
        if invtft:
            return 0, [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    #inverted TitForTatDelayed detection
    invtft = True
    if turns>6:
        for x in range(1,turns-1):
            if history[1,-x] == history[0,-x-2]:
                invtft = False
        if invtft:
            return 0, [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    #openers
    state = '';
    for x in range(1,7):
        if turns >= x:
            state = str(history[0,-x])+str(history[1,-x])+',' + state;

    if state in states:
        #print('\n'+str(history)+'\n'+state+'\n')
        return states[state], [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    #alternating detection
    if turns > 9:
        missed = 0
        for x in range(max(1,turns-9,int(turns*3/4)),turns):
            if history[1,x] == history[1,x-1]:
                missed += 1
        if missed == 0:
            return history[1,-1], [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    if turns > 10 and history[1,-1] == 0 and history[1,-2] == 0 and history[1,-3] == 0 and history[1,-4] == 0:
        positive = 0
        for x in range(1,10):
            if history[1,-x] == 1:
                positive += 1
        if positive == 0:
            return 0, [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    #deadlock breaking
    if dead == deadlock or (dead > deadlock and dead%1 != 0):
        if jossness > 100:
            jossness -= 1
        return 1, [dead+1,rand,abuse,abused,abusePeriod,jossness,forgave]
    elif dead > deadlock:
        return 1, [0,rand,abuse,abused,abusePeriod,jossness,forgave]

    #random detection
    if turns < 20:
        if history[1,-1] != history[0,-1]:
            rand+=1.25
        if turns > 1:
            if history[1,-1] == 1 and history[1,-2] == 1:
                rand-=1.25
            if history[1,-1] != history[1,-2]:
                rand+=0.7
                if turns > 2 and history[1,-1] == history[1,-3]:
                    rand-=0.5

    if abuse <= 0 and (rand > RANDOM if turns < 20 else detectRandom(history)):
        return 0, [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    # deadlock detection
    if turns > 1:
        if history[1,-1] != history[1,-2]:
            dead+=1
        else:
            dead=0
    elif history[1,-1] == 0:
        dead+=1
        rand+=1

    #forgive in DD loop
    if forgave < 2 and turns > 5 and history[1,-1] == 0 and history[1,-2] == 0 and history[1,-3] == 0:
        good = 0
        for x in range(0,turns-3):
            if history[1,x] == 1:
                good +=1
        if good/(turns-3) >= 0.5:
            dead = deadlock+1
            if faults/turns > 0.3:
                forgave += 1
            return 1, [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    #joss detection
    #if turns<35:
    #    print("\njossness: "+str(jossness)+"\nfaults: "+str(faults)+"\n"+str(history[0])+"\n"+str(history[1])+"\n");

    if turns > 5 and history[1,-1] == 0 and history[1,-2] == 0:
        good = 0
        allFaults = 0
        forgivable = 0
        for x in range(1,turns):
            if history[1,x] == 1:
                good +=1
            if history[1,x] != history[0,x-1]:
                faults += 1
                if history[1,x] == 0:
                    forgivable +=1
        if faults > 4:
            jossness = max(0,jossness-100)
        elif allFaults/turns < 0.2:
            dead += 1.5
            if turns > 10:
                jossness += 1
            if good/turns > 0.7 and allFaults/turns < 0.15:
                dead += 1.5
                if turns > 30:
                    jossness += 100
        elif allFaults > 3:
            jossness = 0


    if turns > 5 and history[1,-1] == 0 and history[1,-2] == 1 and history[1,-3] == 0:
        good = 0
        allFaults = 0
        forgivable = 0
        for x in range(1,turns):
            if history[1,x] == 1:
                good +=1
            if history[1,x] != history[0,x-1]:
                faults += 1
                if history[1,x] == 0:
                    forgivable +=1
        if faults > 4:
            jossness = max(0,jossness-100)
        elif allFaults/turns < 0.2:
            dead += 1
            if turns > 10:
                jossness += 1

    #abuse detection
    if abuse == 0 and turns > 2 and turns < 100:
        if np.array_equal(history[1,-5:-1],[1,0,1,1]) and np.array_equal(history[0,-5:-1], [1,1,0,1]):
            abuse = ABUSEVAL
        if np.array_equal(history[1,-5:-1],[1,1,1,1]) and np.array_equal(history[0,-5:-1], [1,0,1,1]):
            abuse = ABUSEVAL-1
        if np.array_equal(history[1,-6:-1],[1,1,0,1,1]) and np.array_equal(history[0,-6:-1], [1,0,1,0,1]):
            abuse = ABUSEVAL

    if abused > 1 and getScore(history,2,turns)/(turns-2.75) < 3:
        abuse = -1
    elif abused > 4 and getScore(history,2,turns)/(turns-2) < 3:
        abuse = -1

    #abuse
    if abuse > 0:
        abuseable = True
        for i in range(0,abuse):
            if turns > i:
                if history[1,-1-i] != 1 or history[0,-1-i] != 1:
                    abuseable = False
        if not abuseable:
            abusePeriod += 1
        elif abuseable and turns > 8:
            abused+=1
            return 0, [dead,rand,abuse,abused,abusePeriod,jossness,forgave]

    #return backupStrategy(history),[dead,rand,abuse,abused,abusePeriod,jossness,forgave]
    return history[1,-1], [dead,rand,abuse,abused,abusePeriod,jossness,forgave]
