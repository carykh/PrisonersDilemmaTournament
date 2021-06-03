import numpy as np

# lambda.py, by Tisajokt (james.and.tisa@gmail.com)
# Honestly a bunch of hastily patched-together code that likely won't generalize too well beyond my test environments

# An OmegaTFT variant (see https://arxiv.org/ftp/cs/papers/0609/0609017.pdf), with improvements:
# - joss detection
# - extortionate ZD detection
# - extra random handling
# - extra alternation handling
# - a snippet of logic inspired by natura.py (made by Josh#6441) for breaking out of mutual defection
# - an extraneous like 8 million different memory slots to track very similar things

# I'm *really* hoping that some people submit joss, ZD extort, random, alternators, etc... otherwise all this work would be for naught
# Excited to see the analysis video and what the winning strategy is!
# Thanks for hosting the tournament Cary, this was awesome! Hope the paper goes well (the deadline confusion sure was a hassle I'm sure)

# Discord community which hosted a GitHub repo & advanced runner environment for this tournament: https://discord.gg/Ymf3PbVNT7

C = 1
D = 0
payoffs = np.array([[1, 5], [0, 3]])
# payoff loops: ("R"andom)
# CC, CC, etc... = 3
# DR, DR, etc... = 3
# CC.1, CC.2, ... CC.n, CD, CC.1... = 3n/(n+1)
# n: 9 (ex. ignoring a 10% joss) = 2.7 (the joss gets 3.2)
# CD, DC, CD, DC, etc... = 2.5
# n: 4 (ex. ignoring a 20% joss) = 2.4 (the joss gets 3.4)
# CC, DD, CC, DD, etc... = 2
# DD, DD, etc... = 1
# RD, RD, etc... = 0.5

# max_joss_rate = (payoffs[C,D]-payoffs[D,C]) / (payoffs[D,C]+payoffs[C,D]-2*payoffs[C,C]) + 1
# in a more readable way: 1 + (S-T) / (S+T -2R)
MAX_JOSS_RATE = 6 # maximum frequency at which a joss can defect before alternating CD-DC becomes better than ignoring joss defections; iff joss hasn't defected in the last <this many> turns, then ignore

DEADLOCK_THRESHOLD = 1

LEAD_DEFECT_RANDOMNESS = 2	# defecting turn 1
COOP_RANDOMNESS	= -1		# cooperating consistently
SWITCH_RANDOMNESS = 1		# switching moves
DIFF_RANDOMNESS = 1			# not playing what I played
TFT_BASED_RANDOMNESS = 1	# not playing tft, & only does so around 50% of the time
RANDOMNESS_THRESHOLD = 5	# threshold to switch to ALLD

FTFT_JOSSNESS = -4			# not responding tft to my defection
BETRAY_JOSSNESS = 1			# betraying after a reward payoff
JOSSNESS_THRESHOLD = 2		# meeting this threshold is necessary but NOT sufficient to classify the opponent as an ignore-able joss

NATURA_WINDOW = 7			# base natura window (cooperate if less than 2 coops within this many past turns)
NATURA_RANDOM_LVL = 0.1		# how close to random the opponent must be before increasing the natura window
NATURA_RANDOM_MOD = 7		# amount natura window is increased
NATURA_GRUDGE_LVL = 10		# no natura if opponent grudged, detected by this many defections in a row

ALTERNATION_THRESHOLD = 7

def strategy(hist, mem):
	turns = hist.shape[1]
	
	# Turn 1: cooperate and initialize memory
	if turns == 0:
		return C, [0, 0, 0, (0, 0), (0, 0, 0), 0, "inactive", (0, 0), (1, [0, 0], 0)]
		
	# Turn 2: play tft, and make note if they defected
	elif turns == 1:
		if hist[1,-1] == D: # opponent led with defection, suspicious
			mem[0] += LEAD_DEFECT_RANDOMNESS
		return hist[1,-1], mem
	
	# A lot of these could probably be integrated together more elegantly and compactly:
	# coop_D, coop_C, tft_deviations, sucker_C, punish_C, my_total_C, coop_rates, and total_D
	randomness = mem[0]
	deadlock = mem[1]
	jossness = mem[2]
	coop_D, coop_C = mem[3]
	successive_defects, successive_coops, successive_alternations = mem[4]
	tft_deviations = mem[5]
	alternator_handler = mem[6]
	sucker_C, punish_C = mem[7]
	my_total_C, coop_rates, total_D = mem[8]
	
	####### TRACKING STUFF: #######
	
	# calculate responsiveness to my moves
	my_total_C += hist[0,-2]
	coop_rates[hist[0,-2]] += hist[1,-1]
	total_D += 1 - hist[1,-1]
	responsiveness = 1
	if my_total_C >= 5 and (turns - my_total_C) >= 5:
		# subtracting probabilities like this is a cardinal sin, forgive me for this
		responsiveness = abs(coop_rates[C] / my_total_C - coop_rates[D] / (turns - my_total_C))
	
	# track deviations from tft
	if hist[1,-1] != hist[0,-2]:
		tft_deviations += 1
		if turns >= 5 and abs(0.5 - tft_deviations / turns) < 0.1:
			randomness += TFT_BASED_RANDOMNESS
	
	# they cooperated twice in a row
	if hist[1,-2] == C and hist[1,-1] == C:
		randomness += COOP_RANDOMNESS
	
	# they didn't respond to my defection
	if hist[0,-2] == D and hist[1,-1] == C:
		jossness += FTFT_JOSSNESS
	
	# track how they respond to reward payoffs...
	prev_moves = (hist[0,-2], hist[1,-2])
	if prev_moves == (C, C):
		if hist[1,-1] == C:
			coop_C += 1
		else:
			coop_D += 1
			jossness += BETRAY_JOSSNESS
	
	# ...and then use that to estimate defection rate, if the opponent were joss
	jossrate = 0.0
	if coop_C + coop_D > 0:
		jossrate = coop_D / (coop_C + coop_D)
	
	# track cooperations after punishment and sucker payoffs, to detect extortionate ZD strategies
	# ex. EXTORT-2 won't cooperate after (D, D), but might cooperate after (C, D)
	if prev_moves == (D, D):
		punish_C += hist[1,-1]
	if prev_moves == (C, D):
		sucker_C += hist[1,-1]
	
	####### ACTUALLY DECIDING MY MOVE: #######
	
	# default: play tft
	move = hist[1,-1]
	
	# standard omegaTFT stuff (cooperation randomness moved to above)
	##### may set move = C (avoid deadlock) #####
	##### may set move = D (take advantage of randoms/unreasonable strategies) #####
	if deadlock >= DEADLOCK_THRESHOLD:
		move = C # we're in deadlock, forgive
		if deadlock == DEADLOCK_THRESHOLD and successive_defects < 2: # ...twice
			deadlock += 1
		else:
			deadlock = 0
	else:
		if hist[1,-1] != hist[1,-2]: # they switched moves
			randomness += SWITCH_RANDOMNESS
		if hist[1,-1] != hist[0,-1]: # they didn't play what I played (yes ik this might seem weird, but it's what the Omega specification says ok?)
			randomness += DIFF_RANDOMNESS
		
		if randomness >= RANDOMNESS_THRESHOLD:
			move = D # this means ALLD from here onwards (unless natura forgiveness activates)
		else:
			if hist[1,-1] != hist[1,-2]: # increment deadlock
				deadlock += 1
			else: # reset deadlock
				deadlock = 0
	
	# if they're unresponsive and cooperate > 70% of the time vs. either move, then exploit
	# this is an extra randomness check on top of Omega's, for strats that are random yet generally cooperative
	##### may set move = D (exploit unresponsive opponents) #####
	if responsiveness < 0.05 and min(coop_rates[D] / (turns - my_total_C), coop_rates[C] / my_total_C) > 0.7:
		move = D
	
	# I'll rely on other strategies to punish joss; imagine that a joss wins cuz everyone's "optimal" and ignores it lol
	##### may set move = C (ignore joss) #####
	if jossness >= JOSSNESS_THRESHOLD and jossrate < 1/MAX_JOSS_RATE and successive_coops >= MAX_JOSS_RATE-1:
		move = C
	
	# track successive moves from opponent
	# tracked AFTER joss handling (since it only applies when a chain of cooperations is broken)
	if hist[1,-1] == C:
		successive_coops += 1
		successive_defects = 0
	else:
		successive_coops = 0
		successive_defects += 1
	
	if hist[1,-1] != hist[1,-2]:
		successive_alternations += 1
	else:
		successive_alternations = 0
	
	# reply TFT if their first defections are in series, which Omega would otherwise try to forgive sometimes bc deadlock threshold = 1
	# eventually overridden by natura forgiveness if their defections persist
	##### may set move = D (small improvement vs. detectives, etc.) #####
	if coop_D == 1 and successive_defects == total_D:
		move = D
	
	# natura window x2 if likely random
	window = NATURA_WINDOW
	if abs(0.5 - tft_deviations / turns) < NATURA_RANDOM_LVL:
		window += NATURA_RANDOM_MOD
	
	# if they seem grudged, it might just be an extortionate ZD player, so check for that
	grudged = False
	if successive_defects >= NATURA_GRUDGE_LVL and not(sucker_C > 0 and punish_C == 0):
		grudged = True
	
	# natura forgiveness, if opponent isn't grudged (and they're not ALLD)
	##### may set move = C (avoid mutual defection) #####
	if total_D < turns and not grudged and turns >= window and sum(hist[0,-window:-1]) + sum(hist[1,-window:-1]) < 2:
		move = C
		# give them a chance to recover their randomness
		randomness = min(randomness, RANDOMNESS_THRESHOLD-1)
	
	# if an opponent alternates (despite my attempt to break deadlock), and they've broken out of an alternation before, then alternate with them
	##### may set move = TFT (idk why but this helps) #####
	if successive_alternations >= ALTERNATION_THRESHOLD:
		if alternator_handler == "broken":
			move = hist[1,-1]
		else:
			alternator_handler = "triggered"
	
	# if they stopped alternating, alternate with them next time
	if alternator_handler == "triggered" and successive_alternations == 0:
		alternator_handler = "broken"
	
	return move, [randomness, deadlock, jossness, (coop_D, coop_C), (successive_defects, successive_coops, successive_alternations), tft_deviations, alternator_handler, (sucker_C, punish_C), (my_total_C, coop_rates, total_D)]

# POWDER #