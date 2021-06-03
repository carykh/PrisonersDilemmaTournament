import numpy as np
import math

# lambda.py, by Tisajokt (james.and.tisa@gmail.com)
# Version 2 (Version 1 was the competition version)

# An OmegaTFT variant (see https://arxiv.org/ftp/cs/papers/0609/0609017.pdf), with improvements:
# - joss detection
# - extortionate ZD detection
# - extra random handling
# - extra alternation handling
# - exploitation of overly forgiving strategies
# - a snippet of logic inspired by natura.py (made by Josh#6441) for breaking out of mutual defection

D = 0
C = 1

MAX_JOSS_RATE = 6				# maximum frequency with which a joss can defect unprovoked, below which it's optimal to ignore them

DEADLOCK_THRESHOLD = 1			# omegaTFT anti-deadlock

LEAD_DEFECT_RANDOMNESS = 2		# defecting turn 1
COOPERATION_RANDOMNESS = -1		# cooperating consistently
SWITCH_RANDOMNESS = 1			# switching moves
DIFF_RANDOMNESS = 1				# not playing what I played
RANDOMNESS_THRESHOLD = 5		# threshold to switch to playing ALLD

NATURA_WINDOW = 7				# if there are fewer than 2 cooperations between both of us in this window of time, cooperate
NATURA_GRUDGE_LVL = 10			# don't cooperate via the above method if the opponent has this many or more defections in a row

EXPLOITABLE_FORGIVENESS = 0.5	# consider opponent exploitable if they forgive at this rate or higher
EXPLOITABLE_DEFECT_STREAK = 3	# maximum defection streak before it's considered unwise to exploit the opponent
EXPLOITATION_DELAY = 7			# turns to wait before attempting exploitation
EXPLOITATIVE_COOP_RATE = 0.25	# minimum accepted temptation cooperation rate from an exploitative opponent
EARLY_FORGIVENESS = 5			# for the first X many turns, always cooperate after opponent's cooperation

def lambda_agent(hist, mem) -> int:
	turns = hist.shape[1]
	
	### turn 1: cooperate & initialize memory ###
	if turns == 0:
		return C, [0, 0, np.array([[0, 0], [0, 0]]), np.array([[0, 0], [0, 0]]), (0, 0, 0), True, False]
	
	### turn 2: play tft ###
	if turns == 1:
		if hist[1,-1] == D:
			mem[1] += LEAD_DEFECT_RANDOMNESS
		return hist[1,-1], mem
	
	deadlock = mem[0]
	randomness = mem[1]
	stimulus = mem[2]
	response = mem[3]
	streak_D, streak_C, streak_alt = mem[4]
	exploitable = mem[5]
	good_faith = mem[6]
	
	##### TRACKING STUFF #####
	
	# decrease randomness if they commit to cooperation
	if hist[1,-2] == C and hist[1,-1] == C:
		randomness += COOPERATION_RANDOMNESS
	
	# track their response to previous moves
	stimulus[hist[0,-2], hist[1,-2]] += 1
	response[hist[0,-2], hist[1,-2]] += hist[1,-1]
	
	# random detection
	stimulus_C = sum(stimulus[C,:])
	stimulus_D = sum(stimulus[D,:])
	response_C = sum(response[C,:])
	response_D = sum(response[D,:])
	total_C = sum(stimulus[:,C]) + hist[1,-1]
	total_D = turns - total_C
	
	# track their streak
	# done AFTER joss handling, which only applies when streak of C is broken
	streak_C_broken = 0
	if hist[1,-1] == D:
		streak_D += 1
		streak_C_broken = streak_C
		streak_C = 0
	else:
		streak_C += 1
		streak_D = 0
	
	# track their alternation streak
	if hist[1,-1] != hist[1,-2]:
		streak_alt += 1
	else:
		streak_alt = 0
	
	# calculate how responsive (tft-like) they are
	# positive value means they're more likely to cooperate after I cooperate
	tftness = 1.0 # 1.0 = tft, 0.0 = random, -1.0 = anti-tft
	if stimulus_C >= 4 and stimulus_D >= 4:
		tftness = response_C / stimulus_C - response_D / stimulus_D
	
	# rate at which they defect after my cooperation
	jossrate = 0.0
	if stimulus_C > 0:
		jossrate = 1 - stimulus_C / stimulus_C
	
	##### DECIDING MY MOVE, TURN 3+ #####
	
	### tft (default) ###
	move = hist[1,-1]
	
	# standard omegaTFT stuff (cooperation randomness moved to above)
	### cooperate (break out of deadlock) ###
	### defect (punish unreasonable opponent) ###
	if deadlock >= DEADLOCK_THRESHOLD:
		move = C
		if deadlock == DEADLOCK_THRESHOLD:# and streak_D < 2:
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
	
	# opponent never cooperates after my defection, defects at an acceptable rate? they're a joss, ignore
	### cooperate (ignore joss) ###
	if stimulus_D >= 2 and response_D == 0 and (streak_C_broken >= 3 or hist[1,-1]) and jossrate <= 1/MAX_JOSS_RATE:
		move = C
	
	# opponent forgives more often than not when I defect? exploit them
	### defect (exploit overly-forgiving opponents) ###
	if stimulus_D >= 1 and (hist[0,-1], hist[1,-1]) == (C, C):
		if exploitable and (response_D / stimulus_D >= EXPLOITABLE_FORGIVENESS or stimulus_D == 1) and (streak_C >= EXPLOITATION_DELAY or np.array_equal(hist[0,-4:], [D,C,D,C]) and np.sum(hist[1,-5:]) >= 4):
			move = D
			randomness -= DIFF_RANDOMNESS
	
	# they're not particularly nice, don't try to exploit them
	if streak_D > EXPLOITABLE_DEFECT_STREAK:
		exploitable = False
	
	### defect (match their first defection streak, ex. small improvement vs. detectives who defect twice in a row) ###
	if total_D > 0 and streak_D == total_D:
		move = D
	
	# detect grudges to avoid pointless forgiveness, but not for exploitative strategies
	grudged = streak_D >= NATURA_GRUDGE_LVL and not(response[D,D] == 0 and response[C,D] > 0 and response[C,D] / stimulus[C,D] >= EXPLOITATIVE_COOP_RATE)
	window = NATURA_WINDOW
	if tftness < 0.1:
		window *= 2
	
	# attempt good-faith cooperation to break out of mutual defection (natura forgiveness)
	# maintain good-faith as long as opponent cooperates
	good_faith = good_faith and (hist[0,-1], hist[1,-1]) == (C, C)
	if tftness > 0 and turns >= window and total_C > 0 and not grudged and sum(hist[0,-window:]) + sum(hist[1,-window:]) < 2:
		good_faith = True
	
	### cooperate (natura forgiveness to avoid mutual defection) ###
	if good_faith:
		move = C
		randomness = min(randomness, RANDOMNESS_THRESHOLD - 1)
	
	# forgive any miscommunications in the first few turns
	### cooperate (early tft after cooperation) ###
	if turns < EARLY_FORGIVENESS and hist[1,-1] == C:
		move = C
	
	# ...and on the 7th turn, increment randomness further if they led with defection (likely random)
	if turns == 7 and hist[1,0] == D and randomness + LEAD_DEFECT_RANDOMNESS >= RANDOMNESS_THRESHOLD:
		move = D
		randomness += LEAD_DEFECT_RANDOMNESS
	
	return move, [deadlock, randomness, stimulus, response, (streak_D, streak_C, streak_alt), exploitable, good_faith]

# the strategy is *technically* a lambda function now
strategy = lambda hist, mem : lambda_agent(hist, mem)
