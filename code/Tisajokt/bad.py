import random
import numpy as np

D = 0
C = 1

def strategy(hist, mem):
	turns = hist.shape[1]
	
	if turns == 0:
		return D, [5, 0]
	
	if turns < 5:
		if hist[1,-1] == C:
			mem[1] += 1
		return D, mem
	
	window = mem[0]
	sucker = mem[1]
	
	sucker -= 0.25
	if hist[1,-1] == C:
		if hist[0,-1] == C:
			window += 2 # oh no, whoops! we cooperated! better wait longer next time
		else:
			sucker += 1.25 # oh no, they're letting themselves be exploited! ig I'll cooperate
	
	move = D
	# try to cooperate after extended mutual defection to let myself be a sucker
	if window < 11 and np.sum(hist[1,-window:]) == 0:
		move = C
	
	# they insist on being a sucker instead, ig I'll cooperate
	if sucker >= 15:
		move = C
		sucker += 0.2
	
	return move, [window, sucker]
