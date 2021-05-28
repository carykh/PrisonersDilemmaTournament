# import numpy as np
#
# # Reminder: For the history array, "tell truth" = 0, "stay silent" = 1
# import random
#
#
def strategy(history, memory=None):
    if len(history[1]) == 0:
        return 1, None
    return history[1, 0], None
