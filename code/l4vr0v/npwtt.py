import numpy


def strategy(history, memory):
    """
    Nice Patient Windowed Tit for Tat (NPWTT):
        1. Nice: Never initiate defection, else face the wrath of the Grudge.
        2. Patient: Respond to defection with defection, unless it was in possibly
            response to my defection. Give opponent a chance to cooperate again since,
            even if they backstab me a few more times, we'll both come out ahead.
            I don't have to worry about this causing my opponent to actually win
            because the Grudge and Tit for Tat will penalize them heavily for
            initiating defection.
        3. Windowed: We don't attempt to cooperate with an opponent that hasn't
            cooperated in the last 5 rounds.
        4. Tit for Tat: (see Patient)

    This strategy generates interesting results. If you look at head-to-head matchups,
    for example, it "loses" to strategies like joss. However, compare that to Tit for
    Tat: Tit for Tat has a low-scoring "win" vs. joss. NPWTT, on the other hand, has
    a high-scoring "loss" vs. joss.

    A cycle of mutual defection is costly because C/C is worth 2 more points than D/D.
    So even if we suffer one D/C (0) for every 2 C/C's (+6), that's still 2 points on
    average for that group of 3, vs. 1 point on average for a series of D/D.
    """
    WINDOW_SIZE = 5
    FREE_PASS = 0  # we forgive if they defect during the first FREE_PASS turns

    num_rounds = history.shape[1]

    opponents_last_move = history[1, -1] if num_rounds >= 1 else 1
    our_second_last_move = history[0, -2] if num_rounds >= 2 else 1

    choice = 1
    if opponents_last_move == 0:
        window_start = max(num_rounds - WINDOW_SIZE, 0)
        window_end = num_rounds
        opponent_recent_moves = history[1, window_start:window_end]
        opponent_recent_stats = dict(
            zip(*numpy.unique(opponent_recent_moves, return_counts=True))
        )
        consider_forgiving = False
        if num_rounds <= FREE_PASS:
            consider_forgiving = True
        elif opponent_recent_stats.get(1, 0) > 0:
            consider_forgiving = True

    # only forgive defections if they've cooperated with us in the past 5 rds
    choice = (
        1
        if (
            opponents_last_move == 1
            or (consider_forgiving and our_second_last_move == 0)
        )
        else 0
    )

    return choice, None
