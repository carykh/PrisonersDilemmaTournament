def strategy(history, memory):
	if history.shape[1] < 1:
		return 0, None
	return 1 - (history[0,-1] ^ history[1,-1]), None