def strategy(history, memory):
    strat = [1,0,1,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1,0]
    address = 0 
    power = 1 
    for f in range(4):
        if history.shape[1] >= f + 1: 
            address += (-(history[1,-f-1]-1) * power) 
        power *= 2 
    for f in range(2): 
        if history.shape[1] >= f + 1:
            address += (-(history[0,-f-1]-1) * power)
        power *= 2
    return strat[address], None
