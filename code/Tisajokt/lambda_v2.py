import numpy as np
import math

# lambda.py, but cleaned up a bit

D = 0
C = 1

MAX_JOSS_RATE = 6

DEADLOCK_THRESHOLD = 1

LEAD_DEFECT_RANDOMNESS = 2
COOPERATION_RANDOMNESS = -1
SWITCH_RANDOMNESS = 1
DIFF_RANDOMNESS = 1
RANDOMNESS_THRESHOLD = 5

NATURA_WINDOW = 7
NATURA_GRUDGE_LVL = 10

def strategy(hist, mem):
	turns = hist.shape[1]
	
	### turn 1: cooperate & initialize memory ###
	if turns == 0:
		return C, [0, 0, np.array([[0, 0], [0, 0]]), np.array([[0, 0], [0, 0]]), (0, 0, 0)]
	
	deadlock = mem[0]
	randomness = mem[1]
	stimuli = mem[2]
	response = mem[3]
	streak_D, streak_C, streak_alt = mem[4]
	
	##### TRACKING STUFF #####
	
	### turn 2: play tft ###
	if turns == 1:
		if hist[1,-1] == D:
			mem[1] += LEAD_DEFECT_RANDOMNESS
		return hist[1,-1], mem
	
	# decrease randomness if they commit to cooperation
	if hist[1,-2] == C and hist[1,-1] == C:
		randomness += COOPERATION_RANDOMNESS
	
	# track their response to previous moves
	stimuli[hist[0,-2], hist[1,-2]] += 1
	response[hist[0,-2], hist[1,-2]] += hist[1,-1]
	
	# track their alternation streak
	if hist[1,-1] != hist[1,-2]:
		streak_alt += 1
	else:
		streak_alt = 0
	
	# calculate how responsive (tft-like) they are
	# positive value means they're more likely to cooperate after I cooperate, negative means less likely, zero means they don't care
	stimuli_C = stimuli[C,C] + stimuli[C,D]
	stimuli_D = stimuli[D,C] + stimuli[D,D]
	tftness = 1.0 # 1.0 = tft, 0.0 = random, -1.0 = anti-tft
	if stimuli_C >= 4 and stimuli_D >= 4:
		tftness = (response[C,C] + response[C,D]) / stimuli_C - (response[D,C] + response[D,D]) / stimuli_D
	
	# rate at which they defect after my cooperation
	jossrate = 0.0
	if stimuli_C > 0:
		jossrate = 1 - (response[C,C] + response[C,D]) / stimuli_C
	
	total_C = stimuli[C,C] + stimuli[D,C] + hist[1,-1]
	total_D = turns - total_C
	
	##### DECIDING MY MOVE, TURN 3+ #####
	
	### tft (default) ###
	move = hist[1,-1]
	
	# standard omega stuff
	### cooperate (break out of deadlock) ###
	### defect (punish unreasonable opponent) ###
	if deadlock >= DEADLOCK_THRESHOLD:
		move = C
		if deadlock == DEADLOCK_THRESHOLD:
			deadlock += 1
		else:
			deadlock = 0
	else:
		if hist[1,-1] != hist[1,-2]:
			randomness += SWITCH_RANDOMNESS
		if hist[1,-1] != hist[0,-1]:
			randomness += DIFF_RANDOMNESS
		
		if randomness >= RANDOMNESS_THRESHOLD:
			move = D
		elif hist[1,-1] != hist[1,-2]:
			deadlock += 1
		else:
			deadlock = 0
	
	### defect (against random/anti-tft opponents) ###
	if tftness <= 0:
		move = D
	
	### cooperate (ignore joss) ###
	if stimuli_D >= 2 and response[D,C] + response[D,D] == 0 and jossrate < 1/MAX_JOSS_RATE and streak_C >= 3:
		move = C
	
	# track their streak
	# done AFTER joss handling, which only applies when streak of C is broken
	if hist[1,-1] == D:
		streak_D += 1
		streak_C = 0
	else:
		streak_C += 1
		streak_D = 0
	
	### defect (better performance vs. detectives, etc.) ###
	if total_D > 0 and streak_D == total_D:
		move = D
	
	grudged = False
	if streak_D >= NATURA_GRUDGE_LVL and not(response[D,D] == 0 and stimuli[C,D] > 0 and response[C,D] / stimuli[C,D] > 0.25):
		grudged = True
	
	window = NATURA_WINDOW
	if tftness < 0.1:
		window *= 2
	
	### cooperate (natura forgiveness to avoid mutual defection) ###
	if tftness > 0 and turns >= window and total_C > 0 and not grudged and sum(hist[0,-window:]) + sum(hist[1,-window:]) < 2:
		move = C
		randomness = min(randomness, RANDOMNESS_THRESHOLD - 1)
	
	# forgive any miscommunications in the first 5 turns
	### cooperate (early tft after cooperation) ###
	if turns < 5 and hist[1,-1] == C:
		move = C
	
	# ...and on the 7th turn, increment it if they lead with defection (likely random)
	if turns == 7 and hist[1,0] == D and randomness + LEAD_DEFECT_RANDOMNESS >= RANDOMNESS_THRESHOLD:
		randomness += LEAD_DEFECT_RANDOMNESS
	
	return move, [deadlock, randomness, stimuli, response, (streak_D, streak_C, streak_alt)]
