import random
import enum


class WhatHappened(enum.Enum):
    just_told_on_him = "because they are nice and i need advantage"
    nothing = None
    told_on_him_again = "hope they won't care"
    stay_silent_pls = "because they are angry"
    stay_lie_pls = "ALWAYS"


def strategy(history, memory):
    US = history[0]
    THEM = history[1]
    gametime = history.shape[1]
    they_bad = len(
        list(filter(lambda x: x == 0, THEM))
    )  # The number of times they cooped
    they_good = len(
        list(filter(lambda x: x == 1, THEM))
    )  # The number of times they bad
    if len(THEM) <= 1 or memory == "WhatHappened.stay_silent_pls":  # Go coop first
        return "stay silent", "WhatHappened.nothing"
    if they_good > they_bad or THEM[-1] == 1:
        if memory in {
            "WhatHappened.just_told_on_him",
            "WhatHappened.told_on_him_again",
        }:  # They don't care if we defect
            return "tell truth", "WhatHappened.told_on_him_again"
        return "stay silent", "WhatHappened.nothing"  # Coop!
    if they_bad > they_good or THEM[-1] == 0:
        if they_good == 0:
            return "tell truth", "WhatHappened.just_told_on_him"
        # if (they_bad / they_good) <= 1.7:
        #     print("random")
        # print(they_bad / they_good)
        if memory == "WhatHappened.just_told_on_him":  # punishment?
            return (
                "stay silent",
                "WhatHappened.told_on_him_again",
            )  # Tests shows, leaving this out gives more luck
        if memory == "WhatHappened.told_on_him_again":  # please cool down
            return "stay silent", "WhatHappened.stay_silent_pls"
        return "tell truth", "WhatHappened.just_told_on_him"
    assert they_bad == they_good
    print("RANDOM")  # on testing, this never runs
    return 0, "WhatHappened.nothing"


# def strategy(history, memory):
#     US = history[0]
#     THEM = history[1]
#     gametime = history.shape[1]
#     they_bad = len(list(filter(lambda x: x == 0, THEM)))
#     they_good = len(list(filter(lambda x: x == 1, THEM)))
#     if len(THEM) <= 1 or memory == WhatHappened.stay_silent_pls:  # Go coop first
#         return "stay silent", WhatHappened.nothing
#     # if they_good == they_bad:
#     #     ...
#     if they_good > they_bad or THEM[-1] == 1:
#         if memory in {
#             WhatHappened.just_told_on_him,
#             WhatHappened.told_on_him_again,
#         }:  # They don't care
#             return "tell truth", WhatHappened.told_on_him_again
#         # if random.random() * 100 < 10:
#         #     return "tell truth", WhatHappened.just_told_on_him
#         return "stay silent", WhatHappened.nothing
#     if they_bad > they_good or THEM[-1] == 0:
#         # if memory == WhatHappened.nothing:
#         #     return "tell truth", WhatHappened.nothing
#         # if they_good == 0:
#         #     return "tell truth", WhatHappened.stay_lie_pls
#         if memory == WhatHappened.told_on_him_again:  # please cool down
#             return "stay silent", WhatHappened.stay_silent_pls
#         if memory == WhatHappened.just_told_on_him:
#             return "stay silent", WhatHappened.nothing
#         return "tell truth", WhatHappened.just_told_on_him
#     assert they_bad == they_good
#     print("RANDOM")
#     return 0, WhatHappened.nothing
# return (
#     THEM[-1] if random.randint(0, 1) == 0 else random.randint(0, 1)
# ), WhatHappened.nothing


# def strategy(history, memory):
#     US = history[0]
#     THEM = history[1]
#     gametime = history.shape[1]
#     they_bad = len(list(filter(lambda x: x == 0, THEM)))
#     they_good = len(list(filter(lambda x: x == 1, THEM)))
#     if len(THEM) <= 1 or memory == WhatHappened.stay_silent_pls:  # Go coop first
#         return "stay silent", WhatHappened.nothing
#     if they_good > they_bad or THEM[-1] == 1:
#         if memory in {
#             WhatHappened.just_told_on_him,
#             WhatHappened.told_on_him_again,
#         }:  # They don't care
#             return "tell truth", WhatHappened.told_on_him_again
#         # if random.random() < 0.10 and they_good == len(THEM):
#         #     return "tell truth", WhatHappened.just_told_on_him
#         # if gametime >= 50 and they_good == len(THEM):
#         #     return "tell truth", WhatHappened.just_told_on_him
#         return "stay silent", WhatHappened.nothing
#     if they_bad > they_good or THEM[-1] == 0:
#         # if memory == WhatHappened.nothing:
#         #     return "tell truth", WhatHappened.nothing
#         # if they_good == 0:
#         #     return "tell truth", WhatHappened.stay_lie_pls
#         if memory == WhatHappened.just_told_on_him:  # punishment?
#             "tell truth", WhatHappened.told_on_him_again
#         if memory == WhatHappened.told_on_him_again:  # please cool down
#             return "stay silent", WhatHappened.stay_silent_pls
#         return "tell truth", WhatHappened.just_told_on_him
#     assert they_bad == they_good
#     return (
#         THEM[-1] if random.randint(0, 1) == 0 else random.randint(0, 1)
#     ), WhatHappened.nothing
# def strategy(history, memory):
#     US = history[0]
#     THEM = history[1]
#     gametime = history.shape[1]
#     they_bad = len(list(filter(lambda x: x == 0, THEM)))
#     they_good = len(list(filter(lambda x: x == 1, THEM)))
#     if len(THEM) <= 1 or memory == WhatHappened.stay_silent_pls:  # Go coop first
#         return "stay silent", WhatHappened.nothing
#     if they_good > they_bad:
#         if memory == WhatHappened.just_told_on_him:  # They don't care
#             return "tell truth", WhatHappened.told_on_him_again
#         # if 40 < gametime:
#         #     return "tell truth", NOne
#         return "stay silent", WhatHappened.nothing
#     else:
#         if memory == WhatHappened.told_on_him_again:
#             return "stay silent", WhatHappened.stay_silent_pls
#         # if memory is True:
#         #     return "stay silent", WhatHappened.nothing
#         return "tell truth", WhatHappened.just_told_on_him
