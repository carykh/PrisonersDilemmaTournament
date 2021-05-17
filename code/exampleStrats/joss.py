import random

# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

# Variant of Tit For Tat that randomly "tells the truth" to try to take advantage
# of overly forgiving opponents.

def strategy(history, memory):
    choice = "stay silent"
    if random.random() < 0.10 or (history.shape[1] >= 1 and history[1,-1] == 0):
    # Choose to tell the truth randomly by 10% chance, OR if and only if the opponent just told the truth.
        choice = "tell truth"
    return choice, None
