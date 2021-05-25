from decimal import Decimal
import random

import numpy as np

def strategy(history, memory):
	
	# A finite state machine detective. 
	# It tries to figure out what the oponent is thinking,
	# and if it cant, it becomes a tit-for-tat
	#
	# TODO list
	# [X] Finite state machine
	# [X] Behave like a tft while detecting
	# [X] Handle randoms
	# [ ] Break out of D/D loops
	# [ ] Detect fibbonachi (ahh how do you spell that)
	# [ ] Maybe swap tft for another variant, unsure as of now
	# [ ] Submit
	#
	# Also, cary if you're reading this a few things:
	# 1. I'd love to see another version if this contest 
	# with a chance of misscomunication, 
	# as well as some other highly requested features
	#
	# 2. Although I doubt i'll win, if I do then I want to explain
	# more about this strategy. *please* contact me so i can
	# explain it to you in more details than I can include in this
	# simple readme.
	#
	# 3. Thanks for hosting such an amazing contest!
	# I met so many cool people though this and the atmosphere
	# inside the discord, with so many wonderful minds working
	# together is truly phenominal. I'm not exagerating when I say
	# that this week has truly changed my life.
	#
	# Thank you. 
	
	num_rounds = history.shape[1] # number of rounds completed
	max_defection_threshold = Decimal(1) / Decimal(2)  # do not forgive high defections
	small_defection_window = 20
	max_local_unprovoked_defections = 5  # too many unprovoked defections? random
	window_start = max(0, num_rounds - small_defection_window) # Set start of detection window
	window_end = num_rounds # end on our current round
	opponents_recent_moves = history[1, window_start + 1 : window_end] #get opponents recent moves
	our_recent_moves = history[0, window_start : window_end - 1] #get our recent moves
	defections = opponents_recent_moves - our_recent_moves # subtract the moves from eachother to get a total number of defections
	opponents_recent_defections = np.count_nonzero(defections == 1) # count the number of defections
	
	if memory == None:
		if num_rounds == 5 or memory == "undecided":
			# Time to choose something.
			opponent_moves = history[1]
			opponent_stats = dict(zip(*np.unique(opponent_moves, return_counts=True)))
			if opponents_recent_defections > max_local_unprovoked_defections:
				# Random Detected
				choice = "defect"
				memory = "alwaysDefect"
			elif opponent_stats.get(0, 0) < 1:  
				# they never defected, take advantage of them
				choice = "defect"
				memory = "alwaysDefect"
			elif opponent_stats.get(0, 0) == 5:  
				# they always defect
				choice = "defect"
				memory = "alwaysDefect"
			elif opponent_moves[2] == 1 and opponent_moves[3] == 0:  
				# ftft detected
				choice = "cooperate"
				memory = "alternate"
			else:
				choice = "cooperate"
				memory = "tft"
		elif num_rounds >= 5:
			# The game has gone on for longer than the testing schedule and we dont have a choice yet, choose tft
			memory = "tft"
		else:
			# We havent picked something yet. We are in testing.
			choice = "cooperate"
			memory = "tft"
	else:
		# We have a chosen state.
		if memory == "tft":
			#do tft
			choice = "cooperate"
			if history.shape[1] >= 1 and history[1,-1] == 0: 
				# Choose to defect if and only if the opponent just defected.
				choice = "defect"
		elif memory == "alternate":
			#alternate
			our_last_move = history[0, -1] if num_rounds > 0 else 1
			choice = 0 if our_last_move else 1
		elif memory == "alwaysDefect":
			if history[1, -1] == "0":
				choice = "cooperate"
				memory = "undecided"
			#always defect
			choice = "defect"
		else:
			print("choice: " + choice)
			print("memory: " + memory)
			choice = "cooperate"
			
	return choice, memory
