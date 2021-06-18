# Strategy designed by Maildropfolder

# Reminder: betray = 0, help friend = 1

# STATSWHALE: Hi! I'm generally a nice guy (bank robbery notwithstanding), but the
# numbers don't lie. Statistically speaking, people hate being taken advantage of,
# but few mind doing each other a solid every now and again. I'll forgive a tattle
# or two (everyone's gotta test the waters, right?), but I never forget a rejection.
# Whales never forget.
# Simply put, the better you've been treating me, the better I treat you.
# True, I won't be farming off of the 'always silent' crowd, but the number of people
# like that in the real world are statistically insignificant. You're better off
# going after 'random response' bots, since they 1) don't have feelings and 2) won't
# react negatively when you constantly steal from them, and 3) will stab you in the
# back when you least expect it.

def getRate(history):
    score = 0
    points = [1, 5, 0, 3]
    for turn in range(history.shape[1]):
        score += points[ (history[0,turn] << 1) + history[1,turn]]
    return score
  
def strategy(history, memory):
    choice = None
    if history.shape[1] == 0:                     # We're on the first turn!
        return 1,(0,-5,0)                       # Make a good first impression
    state, actionAge, rejections = memory  # Load memories
    choice = history[1,-1]                        # When in doubt, Tit-for-tat.
    actionAge += 1
    if actionAge <= 0:
        pass
    elif state == 0: #tit-for-tat
        if rejections < 2 and not choice:
            helps = history[1,-6:].sum()
            if helps < 2:
                state = 2
                choice = 1
                actionAge = 0
            elif helps < 4:
                state = 1
                choice = 1
                actionAge = 0
        elif rejections >= 2 and choice:
            state = -1
            choice = 0
              
    elif state == 1: #attempting cooperation

        if actionAge == 1:
            choice = 1
        elif actionAge > 7:
            helps = history[1,-6:].sum()
            state = 0
            if helps < 4:
                rejections += 1
            
    elif state == 2: #attempting truce
        if actionAge == 1:
            choice = 1
        elif actionAge > 7:
            helps = history[1,-6:].sum()
            state = 0
            if helps < 2:
                rejections += 1
    elif state > -5: #prodding            
        if actionAge > 5 - state/2:
            state = 16 - getRate(history[:,-6:])
            if state > 0:
                state = 0
            else:
                choice = 0
            actionAge = 0
    elif getRate(history[:,-6:]) < 12:
        state = 0
    else:
        choice = 0
   
    return choice, (state, actionAge, rejections)