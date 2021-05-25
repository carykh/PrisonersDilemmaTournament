from decimal import Decimal
import random

import numpy as np

def strategy(history, memory):
	
	# A finite state machine detective. 
	# It tries to figure out what the oponent is thinking,
	# and if it cant, it becomes a tit-for-tat
	
	num_rounds = history.shape[1] # number of rounds completed
	max_defection_threshold = Decimal(1) / Decimal(2)  # do not forgive high defections
	
	if memory == None:
		if num_rounds == 5 or memory == "undecided":
			# Time to choose something.
			opponent_moves = history[1]
			opponent_stats = dict(zip(*np.unique(opponent_moves, return_counts=True)))
			if opponent_stats.get(0, 0) < 1:  
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
