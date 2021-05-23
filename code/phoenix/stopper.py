# Stops when it hits a score of 3

def score(hist):
    lookup = [
        [1, 5],
        [0, 3],
    ]
    score_a = 0
    score_b = 0
    ROUND_LENGTH = hist.shape[1]
    for turn in range(ROUND_LENGTH):
        player_a_move = hist[0, turn]
        player_b_move = hist[1, turn]
        score_a += lookup[player_a_move][player_b_move]
        score_b += lookup[player_b_move][player_a_move]
    return score_a / ROUND_LENGTH, score_b / ROUND_LENGTH


def strategy(hist, _):
    choice = 1
    
    if hist.shape[1] <= 5:
        choice = 1
    if hist.shape[1] != 0:
        my_score, enemy_score = score(hist)

        if my_score > enemy_score and my_score > 3:
            return 0, None
        else:
            choice = hist[1, -1]

            if hist.shape[1] % 20 < 2 and hist[1].sum() != 0:
                choice = 1

    return choice, _
