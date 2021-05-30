# PsiTFT, an OmegaTFT variant with several additions and tweaks for some extra retaliation and forgiveness capabilities

# This version is shamelessly overfitted to the repo

from numpy import ceil

# SCORES[my_move][their_move], defection is 0, cooperation is 1
SCORES = [[1, 5], [0, 3]]

# OmegaTFT parameters
DEADLOCK_THRESHOLD = 1
RANDOMNESS_THRESHOLD = 6

# Revenge attack related parameters
ATTACK_SEQUENCE_DELAYS = [5, 5, 5]
STABILITY_REQUIRED = 2
AGGRESSIVENESS_THRESHOLD = 4
STATUS_CHECK_PERIOD = 20
REMORSE_THRESHOLD = 12

# Forgiveness related related parameters
CALL_FOR_HOPE = 5
COOP_RATIO_WEIGHT = 1.0
COOP_CLOSE_WEIGHT = 0.1
COOP_CLOSE_MEM = 10
HOPELESS_RANDOM_THRESHOLD = 15
TRUCE_CHECK_START = 10

# Cycle checking parameters:
CYCLE_SAMPLE_LENGTH = 50
REPETITION_CHECK_LENGTH = 30
MAX_CYCLE_LENGTH = 20
MIN_CYCLE_LENGTH = 2
HOMOGENEITY_THRESHOLD = 0.15

# Misc
INSTA_ATTACK_PUNISHMENT = 2
BAD_SCORE_THRESHOLD = 2.8
TFT_CHECK_PERIOD = 40

# Attack modes
NOT_ATTACKED = 0
NEVER_ATTACK = -1
WAIT_RETEST = -2
WAIT_ALL_D = -3
WAIT_ALTERNATE = -4
WAIT_ALTERNATE_SOFT = -5
SINGLE_CHECK = 1
DOUBLE_CHECK = 2
ALL_D = 3
ALTERNATE = 4
ALTERNATE_SOFT = 5

# Base strategy modes
OMEGA_TFT = 0
WAIT_TFT = -1
TFT = 1


def strategy(history, memory):

    # Only call when history.shape[1] >= CALL_FOR_HOPE + COOP_CLOSE_MEM
    def is_hopeful():
        coop_ratio = sum(history[1]) / history.shape[1]

        # Get cooperation count in recent history
        coop_close = sum(history[1][-CALL_FOR_HOPE - COOP_CLOSE_MEM: -CALL_FOR_HOPE])

        if coop_ratio * COOP_RATIO_WEIGHT + coop_close * COOP_CLOSE_WEIGHT >= 1:
            return True

        return False

    # This almost never gets used, I guess it does something sometimes
    def check_cycles(cycle_sample_length, rep_check_max, min_cycle_length, max_cycle_length):
        sample = list(history[1][-cycle_sample_length:])
        sample.reverse()

        cycle_found = False
        c_len = min_cycle_length

        while c_len <= max_cycle_length and not cycle_found:
            if all([sample[i] == sample[i + c_len] for i in range(int((ceil(rep_check_max/c_len) - 1) * c_len + 1))]):
                cycle_found = True
            if not cycle_found:
                c_len += 1

        if cycle_found:
            my_sample = history[0][-c_len:]
            return [my_sample, list(sample[:c_len]).reverse()]
        else:
            return None

    def check_avg_score(my_moves, their_moves):
        return sum([SCORES[my_moves[i]][their_moves[i]] for i in range(len(my_moves))]) / len(my_moves)

    def is_homogeneous(sample):
        return min(sum(sample), len(sample) - sum(sample)) < HOMOGENEITY_THRESHOLD * len(sample)

    # Cooperate on the first move
    if history.shape[1] == 0:
        memory = {
            "total_score": 0,
            "average_score": 0,
            "base_strategy_mode": OMEGA_TFT,
            "randomness_counter": 0,
            "deadlock_counter": 0,
            "time_since_first_attack": 0,
            "time_since_last_attack": 0,
            "time_since_strategy_change": 0,
            "time_since_attack_mode": 0,
            "attack_phase": NOT_ATTACKED,
            "attacking": False,
            "hoping": False,
            "hope_broken": False,
            "time_since_truce_check": -1,
            "has_checked_cycles": False,
            "baseline_cycle_score": 0
        }
        return 1, memory

    memory["total_score"] += SCORES[history[0, -1]][history[1, -1]]
    memory["average_score"] = memory["total_score"] / history.shape[1]

    # Play TFT the second round
    if history.shape[1] == 1:
        if history[1, -1]:
            return 1, memory
        else:
            memory["time_since_first_attack"] = 1
            memory["randomness_counter"] += INSTA_ATTACK_PUNISHMENT  # Opponent is suspicious
            return 0, memory

    # Count time since the first defection
    memory["time_since_first_attack"] += memory["time_since_first_attack"] > 0

    # Also count time since my attacks
    memory["time_since_last_attack"] += memory["time_since_first_attack"] > 0
    memory["time_since_attack_mode"] += memory["time_since_attack_mode"] > 0

    if memory["time_since_first_attack"] == history[1, -1] == 0:
        memory["time_since_first_attack"] = 1

    if memory["time_since_attack_mode"] == 0 and memory["attack_phase"] in [ALL_D, ALTERNATE, ALTERNATE_SOFT]:
        memory["time_since_attack_mode"] = 1

    if memory["time_since_attack_mode"] > 0 and memory["attack_phase"] == NEVER_ATTACK:
        memory["time_since_attack_mode"] = 0

    if history[1, -2] == 1 and history[0, -1] == 0:
        memory["time_since_last_attack"] = 1

    if memory["time_since_truce_check"] >= 0:
        memory["time_since_truce_check"] += 1

    # Assuming the opponent is adaptive, check if we're in a looping pattern and TFT is a better response
    # Only do this if the opponent doesn't do the same action almost all the time and the score isn't very good
    if not memory["has_checked_cycles"] and memory["time_since_first_attack"] > CYCLE_SAMPLE_LENGTH and \
            memory["average_score"] <= BAD_SCORE_THRESHOLD and not is_homogeneous(history[1][-CYCLE_SAMPLE_LENGTH:]):
        memory["has_checked_cycles"] = True
        cycles = check_cycles(CYCLE_SAMPLE_LENGTH, REPETITION_CHECK_LENGTH, MIN_CYCLE_LENGTH, MAX_CYCLE_LENGTH)

        if cycles is not None:
            period = len(cycles[0])
            memory["baseline_cycle_score"] = check_avg_score(history[0][-period:], history[1][-period:])

            tft_history = [history[1, -1]]
            tft_history.extend(history[1][-period: -1])
            tft_cycle_score = check_avg_score(tft_history, history[1][-period:])

            if memory["baseline_cycle_score"] < tft_cycle_score:
                memory["base_strategy_mode"] = WAIT_TFT

    if memory["base_strategy_mode"] == WAIT_TFT and history[1, -1] == 1:
        memory["time_since_strategy_change"] = 0
        memory["base_strategy_mode"] = TFT

    if memory["base_strategy_mode"] == TFT:
        if (memory["time_since_strategy_change"] + 1) % TFT_CHECK_PERIOD == 0 and \
                check_avg_score(history[0][-TFT_CHECK_PERIOD:], history[1][-TFT_CHECK_PERIOD:]) < \
                memory["baseline_cycle_score"] or sum(history[1][-TRUCE_CHECK_START:]) == 0:
            # Messed up: let's go back
            memory["base_strategy_mode"] = OMEGA_TFT

        memory["time_since_strategy_change"] += 1
        return history[1, -1], memory

    # Update randomness metric if not in a deadlock and we're not the attackers
    if memory["deadlock_counter"] < DEADLOCK_THRESHOLD and not \
            memory["attack_phase"] in [ALL_D, ALTERNATE, ALTERNATE_SOFT]:
        if history[0, -2] != history[1, -1]:
            memory["randomness_counter"] += 1  # Non TFT behaviour

        if history[1, -2] == history[1, -1]:
            if history[1, -1] == 1:
                memory["randomness_counter"] -= 1  # Reward cooperation
        else:
            memory["randomness_counter"] += 1  # The opponent's move changed, increase randomness counter

    # Attempt to exploit unreactive or forgiving TFT-like defectors that don't surpass the randomness threshold
    if len(history[1]) - sum(history[1]) >= AGGRESSIVENESS_THRESHOLD and memory["attack_phase"] \
            not in [ALL_D, ALTERNATE, ALTERNATE_SOFT]:
        memory["attack_phase"] = NEVER_ATTACK  # Probably not exploitable

    if memory["attack_phase"] == NOT_ATTACKED and memory["time_since_first_attack"] >= ATTACK_SEQUENCE_DELAYS[0]:
        memory["attack_phase"] = SINGLE_CHECK

    if memory["attack_phase"] == WAIT_RETEST and memory["time_since_last_attack"] >= ATTACK_SEQUENCE_DELAYS[1]:
        memory["attack_phase"] = DOUBLE_CHECK

    if memory["attack_phase"] in [WAIT_ALL_D, WAIT_ALTERNATE] and \
            memory["time_since_last_attack"] >= ATTACK_SEQUENCE_DELAYS[2]:
        memory["attack_phase"] = -memory["attack_phase"]

    if memory["attack_phase"] == WAIT_ALTERNATE_SOFT:
        if history[0, -1] == 0:
            return 1, memory
        else:
            if history[1, -1] == 1:  # Go for it
                memory["attack_phase"] = ALTERNATE_SOFT
            else:
                memory["attack_phase"] = NEVER_ATTACK  # Chicken out

            memory["attacking"] = False
            return 1, memory

    if memory["attacking"] and memory["attack_phase"] == SINGLE_CHECK:
        if history[0, -1] == 0 and history[0, -2] == 1:  # Just attacked
            pass
        else:
            if history[0, -2] == 0 and history[1, -1] == 1:  # Go for it
                memory["attack_phase"] = WAIT_RETEST
            else:
                memory["attack_phase"] = WAIT_ALTERNATE_SOFT  # Test this alternative
                return 0, memory

            memory["attacking"] = False
            return 1, memory

    if memory["attacking"] and memory["attack_phase"] == DOUBLE_CHECK:
        if history[0, -1] == 0 and sum(history[0, -3:]) >= 1:  # Just attacked once or twice
            if history[0, -1] == 0 and history[0, -2] == 1:
                return 0, memory
        else:
            if history[0, -2] == 0 and sum(history[1, -2:]) == 2:  # Go for it
                memory["attack_phase"] = WAIT_ALL_D
            elif history[0, -2] == 0 and sum(history[1, -2:]) == 1:  # Go for it kinda
                memory["attack_phase"] = WAIT_ALTERNATE
            else:
                memory["attack_phase"] = NEVER_ATTACK  # Chicken out

            memory["attacking"] = False
            return 1, memory

    # Handle hope mechanic
    if memory["hoping"]:
        if history[0, -1] == 1:  # Just tried to break the cycle
            pass
        elif history[1, -1] == 1:  # Opponent reacted, cooperate twice to reenact cooperation
            memory["hoping"] = False
            memory["deadlock_counter"] = DEADLOCK_THRESHOLD
            memory["randomness_counter"] -= RANDOMNESS_THRESHOLD  # Breather room for defection-cooperation transition
        else:
            memory["hoping"] = False  # Opponent didn't react, keep defecting
            memory["hope_broken"] = True  # Don't try this again; hope is lost

    # If opponent defects too much in a row check if it's redeemable
    if memory["randomness_counter"] <= HOPELESS_RANDOM_THRESHOLD:
        if history.shape[1] >= CALL_FOR_HOPE + COOP_CLOSE_MEM and not memory["hope_broken"] and not memory["hoping"] \
                and sum(history[1][-CALL_FOR_HOPE:]) == 0 and is_hopeful():
            # Give opponent another chance
            memory["hoping"] = True
            memory["attack_phase"] = NEVER_ATTACK
            return 1, memory

        if history.shape[1] >= TRUCE_CHECK_START and 1 in history[1] and sum(history[1, -TRUCE_CHECK_START:]) == 0\
                and memory["time_since_truce_check"] == -1:
            memory["time_since_truce_check"] = 0
            memory["attack_phase"] = NEVER_ATTACK

        # Whoops, opponent isn't as much of a pushover as I thought
        if history.shape[1] >= REMORSE_THRESHOLD + 1 and memory["attack_phase"] in [ALL_D, ALTERNATE] and \
                sum(history[1][-REMORSE_THRESHOLD - 1: -1]) == REMORSE_THRESHOLD and history[1, -1] == 0 \
                and memory["time_since_first_attack"] <= CYCLE_SAMPLE_LENGTH:
            memory["attack_phase"] = NEVER_ATTACK
            memory["deadlock_counter"] = DEADLOCK_THRESHOLD

    if memory["time_since_truce_check"] == 0:
        memory["deadlock_counter"] = DEADLOCK_THRESHOLD
    elif memory["time_since_truce_check"] == 3 and sum(history[1][-2:]):
        memory["time_since_truce_check"] = -1
        memory["randomness_counter"] -= RANDOMNESS_THRESHOLD  # Breather room for defection-cooperation transition

    # Cooperate twice to break deadlocks
    if memory["deadlock_counter"] >= DEADLOCK_THRESHOLD:
        if memory["deadlock_counter"] == DEADLOCK_THRESHOLD:
            memory["deadlock_counter"] += 1
        else:
            memory["deadlock_counter"] = 0

        return 1, memory

    # Full defection mode
    if memory["attack_phase"] == ALL_D:
        return 0, memory

    # Alternated defection modes
    if memory["attack_phase"] in [ALTERNATE, ALTERNATE_SOFT]:
        # Be careful with bad triggers:
        if (memory["time_since_attack_mode"] + 1) % STATUS_CHECK_PERIOD == 0 and check_avg_score(
                history[0][-STATUS_CHECK_PERIOD:], history[1][-STATUS_CHECK_PERIOD:]) <= BAD_SCORE_THRESHOLD:
            memory["attack_phase"] = NEVER_ATTACK

    if memory["attack_phase"] == ALTERNATE:
        return history.shape[1] % 2, memory

    if memory["attack_phase"] == ALTERNATE_SOFT:
        return not history.shape[1] % 5 in [1, 3], memory

    # Core OmegaTFT component
    if memory["randomness_counter"] >= RANDOMNESS_THRESHOLD:  # Opponent seems random or very uncooperative
        return 0, memory
    else:
        if history[1, -1] == 1 and history[1, -2] == 0:
            memory["deadlock_counter"] += 1
        else:
            memory["deadlock_counter"] = 0

        move = history[1, -1]  # Play TFT

    # Look for a counterattack opportunity
    if memory["attack_phase"] in [SINGLE_CHECK, DOUBLE_CHECK] and \
            sum(history[0, -STABILITY_REQUIRED:]) + sum(history[1, -STABILITY_REQUIRED:]) == 2 * STABILITY_REQUIRED:
        memory["attacking"] = True
        return 0, memory

    return move, memory
