import random

# Reminder: For the history array, "tell truth" = 0, "stay silent" = 1

def strategy(history, memory):
    if random.randint(0,1) == 0:
        return "stay silent", None
    else:
        return "tell truth", None
