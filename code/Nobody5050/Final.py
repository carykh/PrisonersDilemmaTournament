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
	# [?] Break out of D/D loops
	# [ ] Detect fibbonachi (ahh how do you spell that)
	# [ ] Maybe swap tft for another variant, unsure as of now
	# [X] Submit
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
	max_local_unprovoked_defections = 6 # too many unprovoked defections? random
	window_start = max(0, num_rounds - small_defection_window) # Set start of detection window
	window_end = num_rounds # end on our current round
	opponents_recent_moves = history[1, window_start + 1 : window_end] #get opponents recent moves
	our_recent_moves = history[0, window_start : window_end - 1] #get our recent moves
	defections = opponents_recent_moves - our_recent_moves # subtract the moves from eachother to get a total number of defections
	opponents_recent_defections = np.count_nonzero(defections == 1) # count the number of defections
	testing_schedule = [1, 0, 0, 1, 1] # list of moves to perform while testing
	
	if memory == None:
		if num_rounds >= len(testing_schedule):
			# Time to choose something.
			opponent_moves = history[1]
			if opponents_recent_defections > max_local_unprovoked_defections:
				# Random Detected
				choice = "defect"
				memory = "defect-assuming-random"
			elif history[1, -1] == 1 and history[1, -2] == 1:
				# they never defected, take advantage of them
				choice = "defect"
				memory = "defect-assuming-cooperative"
			elif history[1, -1] == 0 and history[1, -2] == 0:
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
		else:
			# We havent picked something yet. We are in testing.
			choice = testing_schedule[num_rounds]
	if memory != None:
		# We have a chosen state.
		if memory == "defect-assuming-cooperative":
			# always defect unless they defect
			if opponents_recent_moves[1] == 0:
				choice = "cooperate"
				memory = "tft"
			else:
				choice = "defect"
		elif memory == "tft":
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
			#always defect
			choice = "defect"
		elif memory == "defect-assuming-random":
			# always defect unless they defect thrice in a row, indicating tft behavior (joss)
			choice = "defect"
			if history[1, -1] == 0 and history[1, -2] == 0 and history[1, -3] == 0:
				choice = "cooperate"
				memory = "alwaysCooperate"
		elif memory == "alwaysCooperate":
			choice = "cooperate"
		else:
			choice = "cooperate"
	
	print(memory)		
	return choice, memory
