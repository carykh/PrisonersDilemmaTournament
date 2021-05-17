import random

# Variant of Tit For Tat that randomly defects to try to take advantage
# of overly forgiving opponents.

# Reminder: For the history array, "cooperate" = 1, "defect" = 0

def strategy(history, memory):
    choice = "cooperate"
    if random.random() < 0.10 or (history.shape[1] >= 1 and history[1,-1] == 0):
    # Choose to defect randomly by 10% chance, OR if and only if the opponent just defected.
        choice = "defect"
    return choice, None
