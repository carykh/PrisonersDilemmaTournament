def strategy(history, memory): #It's another Tit for Tat variant! Yay!
    choice = 1
    if len(history[0]) > 1:
        choice = history[1,-1] #Standard Tit for Tat stuff.
        courage = 0 #Oh? What is this??
        for x in range(len(history[0])):
            courage += 2 * history[1][x] - 1 #If the opponent defects, 1 is subtracted, and if the opponent cooperated, 1 is added.
        courage /= len(history[0])  #"Courage" is a simple way to see if the opponent is defecting too much. If it is, this value should be nagative, and if it's about the same it should be near 0, etc.
        if courage < 0 and len(history[0]) > 3: #If it defects a bit too much(the .01 is for detecting random or alternating strategies as well as the strategies which defect more than they cooperate), start defecting.
            choice = 0
    return choice, None
