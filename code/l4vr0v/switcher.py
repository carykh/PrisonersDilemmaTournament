def strategy(history, memory):
    round = history.shape[1]
    GRUDGE = 0
    LASTACTION = 1
    if round == 0:
        mem = []
        mem.append(False)
        mem.append(0)
        return "cooperate", mem
    mem = memory
    if mem[GRUDGE]:
        return "defect", mem
    if round >= 5:
        sin = 0
        for i in range(1, 5):
            if history[1, -i] == 0:
                sin += 1
            if sin == 4:
                mem[GRUDGE] = True
                return "defect", mem
    if mem[LASTACTION] == 0:
        mem[LASTACTION] = 1
        return "cooperate", mem
    else:
        mem[LASTACTION] = 0
        return "defect", mem
