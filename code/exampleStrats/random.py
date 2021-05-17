import random

# Reminder: For the history array, "side with law" = 0, "side with accomplice" = 1

def strategy(history, memory):
    if random.randint(0,1) == 0:
        return "side with accomplice", None
    else:
        return "side with law", None
