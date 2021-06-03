import random

def tft(hist) -> int:
	if hist.shape[1] < 1:
		return 1
	return hist[1,-1]

def joss(hist, rate=0.1) -> int:
	turn = hist.shape[1]
	move = tft(hist)
	if move == 1 and random.random() < rate:
		move = 0
	return move

def strategy(hist, mem):
	if hist.shape[1] < 1:
		return 1, None
	elif hist.shape[1] < 3:
		return hist[1,-1], None
	
	# unless I got the temptation payoff 2 turns ago, play joss
	if (hist[0,-2], hist[1,-2]) != (0, 1):
		return joss(hist), None
	
	# my temptation was unwarranted; if they didn't respond then defect, if they responded then forgive
	if hist[1,-3] == 1:
		return 1 - hist[1,-1], None
	
	# my temptation followed mutual defection or sucker, play tft
	return tft(hist), None