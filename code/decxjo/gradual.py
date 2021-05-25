def strategy(history, memory):
	if memory is None:
		memory = (0, 0)
	defections = memory[0]
	count = memory[1]

	choice = 1
	if count > 0:
		if count < defections:
			choice = 0
			count += 1
		elif count == defections:
			count += 1
		elif count > defections:
			count = 0
	elif history.shape[1] >= 1 and history[1,-1] == 0: # Choose to defect if and only if the opponent just defected.
		defections += 1
		choice = 0
		count = 1

	return choice, (defections, count)