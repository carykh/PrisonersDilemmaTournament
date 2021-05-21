import numpy as np
import random


def repeat(s):
    i = (s + s).find(s, 1, -1)
    return None if i == -1 else s[:i]


def random_test(binary_data: str, verbose=False, block_size=8):
    length_of_binary_data = len(binary_data)
    degree_of_freedom = 6
    pi = [0.01047, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    t2 = (block_size / 3.0 + 2.0 / 9) / 2 ** block_size
    mean = 0.5 * block_size + (1.0 / 36) * (9 + (-1) ** (block_size + 1)) - t2
    number_of_block = int(length_of_binary_data / block_size)
    if number_of_block > 1:
        block_end = block_size
        block_start = 0
        blocks = []
        for i in range(number_of_block):
            blocks.append(binary_data[block_start:block_end])
            block_start += block_size
            block_end += block_size

        complexities = []
        for block in blocks:
            complexities.append(berlekamp(block))

        t = [
            -1.0 * (((-1) ** block_size) * (chunk - mean) + 2.0 / 9)
            for chunk in complexities
        ]
        vg = np.histogram(
            t, bins=[-9999999999, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 9999999999]
        )[0][::-1]
        im = [
            ((vg[ii] - number_of_block * pi[ii]) ** 2) / (number_of_block * pi[ii])
            for ii in range(7)
        ]

        xObs = 0.0
        for i in range(len(pi)):
            xObs += im[i]

        p_value = 1 - np.random.gamma(xObs / 2.0)
        return (p_value, (p_value >= 0.01))
    else:
        return (-1.0, False)


def berlekamp(block_data):
    n = len(block_data)
    c = np.zeros(n)
    b = np.zeros(n)
    c[0], b[0] = 1, 1
    l, m, i = 0, -1, 0
    int_data = [int(el) for el in block_data]
    while i < n:
        v = int_data[(i - l) : i]
        v = v[::-1]
        cc = c[1 : l + 1]
        d = (int_data[i] + np.dot(v, cc)) % 2
        if d == 1:
            temp = np.copy(c)
            p = np.zeros(n)
            for j in range(0, l):
                if b[j] == 1:
                    p[j + i - m] = 1
            c = (c + p) % 2
            if l <= 0.5 * i:
                l = i + 1 - l
                m = i
                b = temp
        i += 1
    return l


def strategy(history, memory):
    choice = 1
    # if not randomOpponent:
    #    randomOpponent = False
    if history.shape[1] > 0:
        p = np.count_nonzero(history[1] == 1) / history.shape[1]
        choice = int(random.random() ** 2 < p)
        if np.all(history[1, -10:] == 0):
            return 0, None

        if len(history[1, -6:]) > 3:
            strPast = "".join(["1" if x == 1 else "0" for x in history[1]])
            r = repeat(strPast[-6:])
            if r == "10" or r == "01":
                choice = 0
            # if history.shape[1] == 16:
            # randomOpponent = random_test(strPast)
    return choice, memory
