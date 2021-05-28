# Detecting Randomness, Increasingly Forgiving Tit-for-tat: Version 21
def strategy(history, memory):

    choice = history[1, -1] if history.shape[1] else 1  # Tit-for-tat
    mem = memory if memory else [[0, 0, 0, 0], False]  # Memory = [[dd, dc, cd, cc], isAlternating]

    if history.shape[1] >= 2:
        mem[0][2 * history[0, -2] + history[1, -1]] += 1  # Update record

    if history.shape[1] >= 10:
        if prob(mem[0]) > max(0.02, 0.95 ** history.shape[1]) and 2.7 ** (history[1] == 0).sum() > 5 * history.shape[1]:
            return 0, mem  # Opponent is acting random so defect

        if (history[1, -8:] == 1).sum() - (history[0, -9:-1] == 1).sum() >= 3:
            return 0, mem  # Not getting punished for defections therefore continue defecting

        if (history.shape[1] >= 40 or history[0, -4] == 0) and history[0, -2] == 0 and not memory[1]:
            return 1, mem  # Forgive if the defection was 'justified'. After 40 rounds become more forgiving

    if history.shape[1] >= 18 and (history[1, -18:] == [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]).all():
        mem[1] = True  # Insanely clever alternating pattern detection

    return choice, mem


def prob(r):  # How unusual this distribution of reactions is assuming our opponent is random
    ex_r = [(r[j] + r[(1 - j) % 4]) * (r[j] + r[(j + 2) % 4]) / sum(r) for j in range(4)]
    x = (sum([(r[i] - ex_r[i]) ** 2 / ex_r[i] if ex_r[i] else 0 for i in range(4)]) / 2) ** (1 / 2)
    return 1 / (1 + 0.278393 * x + 0.230389 * x**2 + 0.000972 * x**3 + 0.078108 * x**4) ** 4
