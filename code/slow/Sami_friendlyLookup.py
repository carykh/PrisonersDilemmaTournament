# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

# The basic idea of the algorithm is to build a lookup table where the previously
# played moves are the keys and value is what was last played by the opponent.
# In general the algorithm assumes the opponent is co-operative and plays with
# "titForTat" -like strategy. The only way the algorithm ever betrays is if the
# opponent starts first.
#
# On top of this, 10 first moves are played with a pure titForTat-strategy to try
# to make the opponent co-operate. Also, there is a detection for "random" play
# that triggers always betray strategy.
#
# On my machine this takes ~2.9 ms per move. If you think that is too much, you can
# drop OPTIMIZE_DEPTH to 5 which takes it down to ~1.2 ms and doesn't seem to
# hurt results too much.
#
# Also sorry for the bad code, this was written as a single evening project.

def strategy(history, memory):
    import numpy
    import math

    # Minimum number of my moves to take decisions on.
    MIN_MY_MOVE_LOOKBACK = 2
    # Maximum number of my moves to take decisions on.
    MAX_MY_MOVE_LOOKBACK = 3
    # Minimum number of opponent moves to take decisions on.
    MIN_YOUR_MOVE_LOOKBACK = 2
    # Maximum number of opponent moves to take decisions on.
    MAX_YOUR_MOVE_LOOKBACK = 3
    # Simulate OPTIMIZE_DEPTH moves forward when making a decision what to play.
    # Higher value = longer decision time and better results (maybe).
    OPTIMIZE_DEPTH = 6
    # Index 0 = co-operate. Index 1 = betray.
    CHOICE_TABLE = ["tell truth", "stay silent"]
    # Scores for different combinations of co-operate and betray.
    RESULT_TABLE = numpy.zeros((2, 2), dtype=int)
    RESULT_TABLE[0][0] = 1
    RESULT_TABLE[0][1] = 5
    RESULT_TABLE[1][0] = 0
    RESULT_TABLE[1][1] = 3

    if memory == None:
        memory = dict()
        lookup = [[numpy.zeros((2**my, 2**your, 2), dtype=int) for your in range(MAX_YOUR_MOVE_LOOKBACK + 1)] for my in range(MAX_MY_MOVE_LOOKBACK + 1)]
    else:
        lookup = memory["lookup"]

    memory["lookup"] = lookup
    time = history.shape[1]

    # Calculate what data the opponent took the last decision on.
    # Last turn is ignored because opponent couldn't know what I would
    # have played.
    # Least significant bit = the most recent turn
    my_value = 0
    for i in range(min(time - 1, MAX_MY_MOVE_LOOKBACK)):
        my_value += 2**i * history[0][-i - 2]
    your_value = 0
    for i in range(min(time - 1, MAX_YOUR_MOVE_LOOKBACK)):
        your_value += 2**i * history[1][-i - 2]

    # Write to lookup table the opponent decision.
    if time >= 2:
        last_your = history[1][-1]

        for my in range(min(time - 1, MAX_MY_MOVE_LOOKBACK + 1)):
            for your in range(min(time - 1, MAX_YOUR_MOVE_LOOKBACK + 1)):
                # Mask out irrelevant turns
                my_mask = (2 ** my) - 1
                your_mask = (2 ** your) - 1

                lookup[my][your][my_value & my_mask][your_value & your_mask][last_your] = time

    # Add last turn information for making a decision this turn.
    if time >= 1:
        my_value = my_value * 2 + history[0][-1]
        your_value = your_value * 2 + history[1][-1]

    # Try to detect if opponent is playing "randomly" by finding contradicting moves.
    num_random = 0
    for my_possible in range(2**MAX_MY_MOVE_LOOKBACK):
        for your_possible in range(2**MAX_YOUR_MOVE_LOOKBACK):
            if (lookup[MAX_MY_MOVE_LOOKBACK][MAX_YOUR_MOVE_LOOKBACK][my_possible][your_possible][0] != 0
                and lookup[MAX_MY_MOVE_LOOKBACK][MAX_YOUR_MOVE_LOOKBACK][my_possible][your_possible][1] != 0):
                num_random += 1
    if num_random >= 9:
        return CHOICE_TABLE[0], memory

    # Check lookup table for what the opponent probably plays based on the simulated moves.
    def find_answer(my_simulated_value, your_simulated_value):
        for my in range(MAX_MY_MOVE_LOOKBACK, MIN_MY_MOVE_LOOKBACK - 1, -1):
            for your in range(MAX_YOUR_MOVE_LOOKBACK, MIN_YOUR_MOVE_LOOKBACK - 1, -1):
                my_mask = (2 ** my) - 1
                your_mask = (2 ** your) - 1

                last_betray = lookup[my][your][my_simulated_value & my_mask][your_simulated_value & your_mask][0]
                last_coop = lookup[my][your][my_simulated_value & my_mask][your_simulated_value & your_mask][1]

                if (last_betray == 0 and last_coop != 0) or last_coop > last_betray:
                    return 1
                elif (last_coop == 0 and last_betray != 0) or last_betray > last_coop:
                    return 0
        # If unknown, assume tit-for-tat.
        return my_simulated_value & 1

    # Calculate the expected score for a move sequence.
    def simulate(future):
        if time >= 1:
            my_simulated_value = my_value
            your_simulated_value = your_value
        else:
            my_simulated_value = 0
            your_simulated_value = 0

        score = 0

        for i in range(OPTIMIZE_DEPTH):
            my_play = future & 1
            your_play = find_answer(my_simulated_value, your_simulated_value)
            future //= 2
            score += RESULT_TABLE[my_play][your_play]

            my_simulated_value = my_simulated_value * 2 + my_play
            your_simulated_value = your_simulated_value * 2 + your_play

        return score
    
    best_play = 0
    best_play_score = 0

    my_mask = (2 ** MAX_MY_MOVE_LOOKBACK) - 1
    your_mask = (2 ** MAX_YOUR_MOVE_LOOKBACK) - 1
    if time < 10:
        # Play first 10 turns with titForTat strategy.
        best_play = history[1][-1] if time > 0 else 1
    else:
        for future in range(2**OPTIMIZE_DEPTH):
            result = simulate(future)
            my_play = future & 1

            my_intention = (my_value * 2 + my_play) & my_mask
            your_intention0 = (your_value * 2) & your_mask
            your_intention1 = (your_value * 2 + 1) & your_mask

            # def not_seen_in_a_long_time(a, b, c):
            #     return lookup[MAX_MY_MOVE_LOOKBACK][MAX_YOUR_MOVE_LOOKBACK][a][b][c] == 0

            # If we've not tried co-operating in this situation, encourage trying it.
            # This does not seem to work well, so taken out...
            # if (not_seen_in_a_long_time(my_intention, your_intention0, 0)
            #     and not_seen_in_a_long_time(my_intention, your_intention0, 1)
            #     and not_seen_in_a_long_time(my_intention, your_intention1, 0)
            #     and not_seen_in_a_long_time(my_intention, your_intention1, 1)) and my_play == 1:
            #     result += OPTIMIZE_DEPTH * 2

            if result > best_play_score:
                best_play = my_play
                best_play_score = result

    return CHOICE_TABLE[best_play], memory
