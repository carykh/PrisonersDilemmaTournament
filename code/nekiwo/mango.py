import numpy as np

# Licensed under MIT in https://github.com/Prisoners-Dilemma-Enjoyers/PrisonersDilemmaTournament
# Member(owner) of the Unofficial Prisoner's Dilemma Discord server  https://discord.gg/6UBBKxyk
# Big thanks to everyone who participated in our server, it was a very fun week

# My shamelessly stolen version of OTFT
# from https://arxiv.org/ftp/cs/papers/0609/0609017.pdf

# Includes a lot of small improvements
# (It's really hard to improve this strat without ruining it)

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


def TFTCheck(history):
    MyMoves = history[0, -4:]
    EnemyMoves = history[1, -4:]
    
    if history.shape[1] > 4 and \
       np.array_equal(EnemyMoves, [0, 1, 0, 0]) and \
       np.array_equal(MyMoves, [0, 0, 1, 0]):

        return False
    
    return True


def NicePeriodicJoss(history):
    choice = 1

    if history.shape[1] > 0 and history[1, -1] == 0:
        choice = 0

        if history.shape[1] % 20 < 2 and history[1].sum() != 0:
            choice = 1

    return choice


def tft(history):
    choice = 1

    if history.shape[1] > 0 and history[1, -1] == 0:
        choice = 0

    return choice
            

def strategy(history, memory):

    # Standard OTFT stuff

    RandomThreshold = 5
    DeadlockThreshold = 1

    randomness = 0
    deadlock = 0

    if memory == None:
        memory = [randomness, deadlock]
    else:
        randomness = memory[0]
        deadlock = memory[1]

    # This TFT alternative works much better than with regular TFT
    choice = NicePeriodicJoss(history)

    # One of the improvemnts which checks in case the first move was defect
    # Random has a 50% chance of doing it, this is very big red flag
    if history.shape[1] == 1 and history[1, -1] == 0:
        randomness += 4

    if history.shape[1] > 1:
        if deadlock >= DeadlockThreshold:
            choice = 1

            if deadlock == DeadlockThreshold:
                deadlock += 1
            else:
                deadlock = 0

        else:
            # Adjusting those values improved random detection by 0.003 - 0.010 points on average
            # Makes it easier to find actual random from Joss-likes
            if history[1, -1] == history[1, -2] == 1:
                randomness -= 1.25

            elif history[1, -1] == history[1, -2] == 0:
                randomness -= 0.25

            if history[1, -1] != history[1, -2]:
                randomness += 1

            if history[0, -1] != history[1, -1]:
                randomness += 1.25

            if history[1, -1] != history[0, -2]:
                randomness += 0.75

            # Checks for certain pattern that a TFT will never do
            # Rare occurence, but a big sign of random
            if not TFTCheck(history):
                randomness += 2

            # Checks if patterns are similar to Joss-likes
            # Random has a chance of doing this accidentally so I'm not taking away a lot of points
            if history.shape[1] > 8 and DetectJoss(history, 8):
                randomness -= 0.25


            if randomness >= RandomThreshold:
                choice = 0

            else:

                if history[1, -1] != history[1, -2]:
                    deadlock += 1
                else:
                    deadlock = 0

                # First 10 rounds are TFT to prevent triggering detectives
                if history.shape[1] < 10:
                    choice = tft(history)


            

    memory = [randomness, deadlock]

    return choice, memory

    # Thanks Cary!!
