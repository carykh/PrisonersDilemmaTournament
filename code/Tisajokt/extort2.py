import random

table = {
	(1, 1): 7.0/8.0,
	(1, 0): 7.0/16.0,
	(0, 1): 3.0/8.0,
	(0, 0): 0
}
def strategy(history, memory):
	if history.shape[1] < 1:
		return 1, None
	
	if random.random() < table[(history[0,-1], history[1,-1])]:
		return 1, None
	else:
		return 0, None