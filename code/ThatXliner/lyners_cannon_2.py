# pylint: disable=C,W,R
# type: ignore
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
        if memory == "WhatHappened.just_told_on_him":  # punishment?
            return "tell truth", "WhatHappened.told_on_him_again"
        # Tests shows, leaving the above out gives more luck

        # But that means this logically shouldn't run... but other algorithms make it run
        if memory == "WhatHappened.told_on_him_again":  # please cool down
            return "stay silent", "WhatHappened.stay_silent_pls"
        return "tell truth", "WhatHappened.just_told_on_him"
    assert they_bad == they_good
    print("RANDOM")  # on testing, this never runs
    return 0, "WhatHappened.nothing"
