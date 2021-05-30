import numpy as np

'''
We use a derivation of the TitForTat-Strategy to force the enemy into cooperating if he wants to maximize his overall 
score. Moreover forgiving elements can be found in addition to counter measurements against detective and random strategies

We start with the state "detective_phase" that represents a TitForTat play to convince the enemy into cooperating. 
Furthermore this state is established after every friendly_sequence of 100% cooperating moves to block any new unsought 
investigations.

If we are not in such a phase we play as forgiving as humanly possible, i.e. after a cycle of switching moves [DC][CD] 
we again to break escalation spirals asap. This however only happens a maximum of max_forgiving times in row, if the distance 
is lower or equal to min_distance_forgiving for each of these cycles. In case of such an event, we continue to play a non forgiving TitForTat 
and won't activate a new detective phase after this (because it does not fall into a deeply planned strategy to play
this pattern). The counter resets after another friendly_sequence.

Over the course of the whole game we investigate the "negativeness" of all moves after the first detective phase. This is 
done by measuring the deviation between the opponent and TitForTat. If we examined more than random_sequence moves and 
the ratio of "unintuitive" moves is greater or equal to the acceptable_deviation we start defecting until this ratio 
is bad.
'''

#memory = [string: "modus", int: distanceforgiving, int: numberforgiving, int: detectivephase, list: titfortatarray]

def strategy(history, memory):
    # initializing variables and memory
    detective_phase = 5
    friendly_sequence = 7
    random_sequence = 10
    max_forgiving = 3
    min_distance_forgiving = 4
    acceptable_deviation = 0.5
    choice = "cooperate"
    round = history.shape[1]
    if memory == None:
        memory = ["TitForTat", 0, 0, detective_phase, []]

    #checking the modus to determine our strategy
    if memory[0] == "TitForTat" and history.shape[1] >= 1:
        choice = history[1, -1]
    elif memory[0] == "ForgivingTitForTat":
        choice = history[1, -1]
        if history[0, -2] == 0 and history[0, -1] == 1 and history[1, -2] == 1 and history[1, -1] == 0:
            choice = "cooperate"
            if round - memory[1] <= min_distance_forgiving:
                memory[2] += 1
            else:
                memory[2] = 0
            memory[1] = round
    elif memory[0] == "Defect":
        choice = "defect"

    #activating the modus
    #detection of a friendly_sequence (10 consecutive cooperations)
    if round >= friendly_sequence:
        reset = True
        for i in range(1, 1 + friendly_sequence):
            if not (history[0, -i] == 1):
                reset = False
        if reset:
            memory = ["TitForTat", 0, 0, detective_phase, memory[4]]
    #end of the detective_phase
    if memory[0] == "TitForTat":
        memory[3] -= 1
        if memory[3] == 0:
            memory[0] = "ForgivingTitForTat"
    #end of Forgivingphase
    if memory[2] >= max_forgiving:
        memory[0] = "TitForTat"
    #detection of a random or hyperaggressive player
    if round >= random_sequence + detective_phase:
        deviation = memory[4] - history[1, detective_phase:]
        deviation_rate = 1 - np.count_nonzero(deviation == 0) / len(deviation)
        if deviation_rate >= acceptable_deviation:
            memory[0] = "Defect"
    if round >= detective_phase:
        memory[4].append(history[0, -1])

    return choice, memory