def strategy(history, memory):
	deadlockThreshold = 1
	randomnessThreshold = 5

	if history.shape[1] == 0:
		return 1, (0, 0, False, False)
	if history.shape[1] == 1:
		return history[1,-1], (0, 0, False, False)

	deadlock = memory[0]
	randomness = memory[1]

	opponentLast = history[1,-1]
	opponentPrevious = history[1,-2]
	myLast = history[0,-1]

	choice = 1

	if deadlock >= deadlockThreshold:
		choice = 1
		if deadlock == deadlockThreshold:
			deadlock += 1
		else:
			deadlock = 0
	else:
		if opponentLast == 1 and opponentPrevious == 1:
			randomness -= 1
		if opponentLast != opponentPrevious:
			randomness += 1
		if opponentLast != myLast:
			randomness += 1

		if randomness >= randomnessThreshold:
			choice = 0
		else:
			choice = opponentLast

			if opponentLast != opponentPrevious:
				deadlock += 1
			else:
				deadlock = 0

	return choice, (deadlock, randomness, False, False)