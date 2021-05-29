import numpy


def strategy(history, memory):
    """
    Nice Patient Reflective Tit for Tat with Half-Life threshold and Random Aware
    (NPRTTHLRA):
        1. Nice: Never initiate defection, else face the wrath of the Grudge.
        2. Patient: Respond to defection with defection, unless it was in possibly
            response to my defection. Give opponent a chance to cooperate again since,
            even if they backstab me a few more times, we'll both come out ahead.
            I don't have to worry about this causing my opponent to actually win
            because the Grudge and Tit for Tat will penalize them heavily for
            initiating defection.
        3. Reflective: Before cooperating in forgiveness, we check whether the opponent
            has defected so far more than 1/2 of the time. If they have, then we'd
            probably lose out by cooperating.
        4. Half-Life: Using decayed half life to 0.5 for defection threshold.
        5. Random-Aware: Aware with random by detecting unprovoked defection.
        4. Tit for Tat: (see Patient)

    This strategy generates interesting results. If you look at head-to-head matchups,
    for example, it "loses" to strategies like joss. However, compare that to Tit for
    Tat: Tit for Tat has a low-scoring "win" vs. joss. NPRTT, on the other hand, has
    a high-scoring "loss" vs. joss.

    A cycle of mutual defection is costly because C/C is worth 2 more points than D/D.
    So even if we suffer one D/C (0) for every 2 C/C's (+6), that's still 2 points on
    average for that group of 3, vs. 1 point on average for a series of D/D. This also
    guides the 1/2 cutoff for the Reflective trait.
    """
    HALF_LIFE = 20
    STEADY_THRESHOLD = 1 / 2
    DECAY_MULTIPLIER = 1 - STEADY_THRESHOLD 
    LONG_WINDOW = 16
    UNPROVOKED_DEFECTION_RATE_THRESHOLD = 0.4

    num_rounds = history.shape[1]

    opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
    our_second_last_move = history[0, -2] if num_rounds >= 2 else 1

    # random handler
    if memory == None:
        # store memory fighting random
        memory = False
    
    if not memory:
        if num_rounds >= LONG_WINDOW:
            our_shifted_move = numpy.append([0], history[0, :-1])
            opponent_moves = history[1, :]

            diff = our_shifted_move - opponent_moves 
            unprovoked_defections_rate = (diff == 1).sum() / num_rounds

            # too much unprovoked defection
            if unprovoked_defections_rate > UNPROVOKED_DEFECTION_RATE_THRESHOLD:
                memory = True
    
    if memory:
        choice = 0
        return choice, memory

    # if opponent defects more often, then screw 'em
    MAX_DEFECTION_THRESHOLD = STEADY_THRESHOLD + DECAY_MULTIPLIER * numpy.power(0.5,(num_rounds/HALF_LIFE))

    opponent_history = history[1, 0:num_rounds]
    if num_rounds == 0:
        opponent_defection_rate = 0
    else:
        opponent_stats = dict(zip(*numpy.unique(opponent_history, return_counts=True)))
        opponent_defection_rate = int(opponent_stats.get(0, 0)) / num_rounds

    be_patient = opponent_defection_rate <= MAX_DEFECTION_THRESHOLD

    choice = (
        1
        if (opponents_last_move == 1 or (be_patient and our_second_last_move == 0))
        else 0
    )

    return choice, memory