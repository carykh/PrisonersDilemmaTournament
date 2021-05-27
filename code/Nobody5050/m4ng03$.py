import numpy as np

# Licensed under MIT in https://github.com/Prisoners-Dilemma-Enjoyers/PrisonersDilemmaTournament

# A modification of https://github.com/Prisoners-Dilemma-Enjoyers/PrisonersDilemmaTournament/blob/main/code/nekiwo/ShirtlessMangos.py by nobody6502
# includes ftft detection, and uses balance instead of tft

def DetectJoss(history, window):
    AlignMe1 = history[0, -window:]
    AlignEnemy1 = history[1, -window - 1:-1]

    AlignMe2 = history[0, -window - 1:-1]
    AlignEnemy2 = history[1, -window:]

    if np.count_nonzero(np.absolute(AlignMe1 - AlignEnemy1) == 1) < np.floor(window / 3) or \
        np.count_nonzero(np.absolute(AlignMe2 - AlignEnemy2) == 1) < np.floor(window / 3):
        # Oof, it's TFT/Joss
        return True

    return False


def tft(history):
	choice = 1
	if history.shape[1] != 0:
		percents = np.mean(history, axis=1)
		if percents[0] > percents[1] + 0.1:
			choice = 0
	return choice

def strategy(history, memory):

    # Standard OTFT stuff

    RandomThreshold = 5
    DeadlockThreshold = 1

    randomness = 0
    deadlock = 0
    ftft = 0
    
    # for ftft detection
    num_rounds = history.shape[1]
    opponent_moves = history[1]
    
    if memory == None:
        memory = [randomness, deadlock, ftft]
    else:
        randomness = memory[0]
        deadlock = memory[1]
        ftft = memory[2]

    # I tried many, many alternative but regular TFT works the best anyway
    #LIES! PeriodicCopycat is used instead
    choice = tft(history)

    # One of the improvemnts which checks in case the first move was defect
    # Random has a 50% chance of doing it, this is very big red flag
    if history.shape[1] == 1 and history[1, -1] == 0:
        randomness += 2

    if history.shape[1] > 1:
        if deadlock >= DeadlockThreshold and ftft != 1:
            choice = 1

            if deadlock == DeadlockThreshold:
                deadlock += 1
            else:
                deadlock = 0

        else:
            if history[1, -1] == history[1, -2] == 1:
                # Adjusting those values improved random detection by 0.003 - 0.010 points on average
                # Makes it easier to find actual random from Joss-likes
                randomness -= 1.25

            if history[1, -1] != history[1, -2]:
                randomness += 1

            if history[0, -1] != history[1, -1]:
                randomness += 1.25

            # Checks if patterns are similar to Joss-likes
            # Random has a chance of doing this accidentally so I'm not giving it a lot of points
            if history.shape[1] > 8 and DetectJoss(history, 8):
                randomness -= 0.25


            if randomness >= RandomThreshold:
                choice = 0
            else:

                if history[1, -1] != history[1, -2]:
                    deadlock += 1
                else:
                    deadlock = 0
            	
            if num_rounds > 3:
            	if opponent_moves[2] == 1 and opponent_moves[3] == 0:
            		# ftft detected
            		our_last_move = history[0, -1] if num_rounds > 0 else 1
            		choice = 0 if our_last_move else 1
            		ftft = 1

    memory = [randomness, deadlock, ftft]

    return choice, memory

    # Thanks Cary!!
