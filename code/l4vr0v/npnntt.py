def strategy(history, memory):
    """
    Nice Patient Non-Naive Tit for Tat (NPNNTT):
        1. Nice: Never initiate defection, else face the wrath of the Grudge.
        2. Patient: Respond to defection with defection, unless it was in possibly
            response to my defection. Give opponent a chance to cooperate again since,
            even if they backstab me a few more times, we'll both come out ahead.
            I don't have to worry about this causing my opponent to actually win
            because the Grudge and Tit for Tat will penalize them heavily for
            initiating defection.
        3. Non-Naive: We don't attempt to cooperate with an opponent that has never
            cooperated with us before. (This prevents us from being repeatedly burned
            by Always Defect.)
        4. Tit for Tat: (see Patient)

    This strategy generates interesting results. If you look at head-to-head matchups,
    for example, it "loses" to strategies like joss. However, compare that to Tit for
    Tat: Tit for Tat has a low-scoring "win" vs. joss. NPNNTT, on the other hand, has
    a high-scoring "loss" vs. joss.

    A cycle of mutual defection is costly because C/C is worth 2 more points than D/D.
    So even if we suffer one D/C (0) for every 2 C/C's (+6), that's still 2 points on
    average for that group of 3, vs. 1 point on average for a series of D/D.
    """
    num_rounds = history.shape[1]

    opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
    our_second_last_move = history[0, -2] if num_rounds >= 2 else 1

    # only forgive defections if they've cooperated with us before
    choice = (
        1
        if (opponents_last_move == 1 or (memory is True and our_second_last_move == 0))
        else 0
    )
    # in memory, we track whether the opponent has cooperated with us at least once
    memory = (
        True
        if (history.shape[1] > 0 and opponents_last_move == 1 or memory is True)
        else False
    )

    return choice, memory
