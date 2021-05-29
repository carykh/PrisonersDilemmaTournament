# Reminder: For the history array, "cooperate" = 1, "defect" = 0

def strategy(history, memory):
    TIE_BREAKER_LIMIT = 3

    # store tie-breaker counter
    if memory == None:
        memory = 0

    # default cooperate
    choice = 1

    # revenge
    if history.shape[1] >= 1:
        # if enemy defected revange
        if history[1,-1] == 0: 
            choice = 0

    # forgive
    if history.shape[1] >= 2 and choice == 0:
        # forgive if their defect because of our defect when they are not
        if history[0, -1] == 1 and history[0, -2] == 0 and history[1, -2] == 1:
            # [
            #   [0, 1],
            #   [1, X]
            # ]
            choice = 1

        # forgive (tieBreaker) if both have been defecting two times in a row
        if memory < TIE_BREAKER_LIMIT:
            if (history[0, -1] == 0 
            and history[0, -2] == 0 
            and history[1, -1] == 0
            and history[1, -2] == 0):
                # [
                #   [0, 0],
                #   [0, 0]
                # ]
                choice = 1
                memory += 1

    return choice, memory
