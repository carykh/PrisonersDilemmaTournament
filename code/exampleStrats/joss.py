import random

# Reminder: For the history array, "side with law" = 0, "side with accomplice" = 1

# Variant of Tit For Tat that randomly defects to try to take advantage
# of overly forgiving opponents.

def strategy(history, memory):
    choice = "side with accomplice"
    if random.random() < 0.10 or (history.shape[1] >= 1 and history[1,-1] == 0):
    # Choose to side-with-law randomly by 10% chance, OR if and only if the opponent just defected.
        choice = "side with law"
    return choice, None
