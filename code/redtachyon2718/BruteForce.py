thinklength = 5

howahead = 3

LearnRate= 0.05

LearnIterations = 30

LearnThreshold = 1e-3

table = [[1,5],[0,6]]

import random as r

import time as t

alert = 20

alertatall = False

def activation(x):
    if(x > 0):
        return x
    else:
        return x / 1024

def clone(thing):
    if(type(thing) == list):
        a = []
        for x in range(len(thing)):
            a.append(clone(thing[x]))
        return a
    else:
        return thing

def derivative(x):
    if x > 0:
        return 1
    else:
        return 1 / 1024

class network:
    def __init__(self,nodes):
        self.nodes = []
        self.raw = []
        self.weights = []
        self.biases = []
        a = []
        self.CostValue = 1000
        for x in range(nodes[0]):
            a.append(0)
        self.nodes.append(a)
        self.raw.append(a)
        for x in range(len(nodes) - 1):
            self.nodes.append([])
            self.raw.append([])
            self.biases.append([])
            self.weights.append([])
            for y in range(nodes[x + 1]):
                self.raw[x + 1].append(0)
                self.nodes[x + 1].append(0)
                self.biases[x].append(r.random())
                self.weights[x].append([])
                for z in range(nodes[x]):
                    self.weights[x][y].append(r.random())

    def predict(self,input_list):
        self.nodes[0] = input_list
        self.raw[0] = input_list
        for x in range(len(self.biases)):
            a = []
            c = []
            for y in range(len(self.biases[x])):
                b = self.biases[x][y]
                for z in range(len(self.weights[x][y])):
                    b += self.weights[x][y][z] * self.nodes[x][z]
                a.append(activation(b))
                c.append(b)
            self.nodes[x + 1] = a
            self.raw[x + 1] = c

    def output(self):
        return self.nodes[len(self.nodes) - 1]

    def cost(self,input_list,output_list):
        self.predict(input_list)
        a = self.output()
        b = 0
        for x in range(len(a)):
            try:
                b += ((a[x] - output_list[x]) ** 2)
            except OverflowError:
                b += 16e+256
        self.CostValue = b
        return b

    def backprop(self, input_list, output_list):
        self.predict(input_list)
        w = clone(self.weights)
        b = clone(self.biases)
        expectedoutput = output_list
        for p in range(len(self.nodes) - 1):
            x = len(self.nodes) - p - 1
            differences = []
            for y in range(len(self.nodes[x])):
                differences.append(self.nodes[x][y] - expectedoutput[y])
            for y in range(len(self.nodes[x])):
                b[x - 1][y] = 2 * differences[y] * derivative(self.raw[x][y])
                for z in range(len(self.nodes[x - 1])):
                    w[x - 1][y][z] = self.nodes[x - 1][z] * 2 * differences[y] * derivative(self.raw[x][y])
            expectedoutput = []
            for y in range(len(self.nodes[x - 1])):
                a = 0
                for z in range(len(self.nodes[x])):
                    a += self.weights[x - 1][z][y] * 2 * differences[z] * derivative(self.raw[x][z])
                expectedoutput.append(((a / len(self.nodes[x])) / (-2)) + self.nodes[x - 1][y])
        return [w,b]

    def train(self,inputs,outputs,LearnRate,iterations):
        for q in range(iterations):
            total = 0
            c = self.backprop(inputs,outputs)
            avgCost = self.cost(inputs,outputs)
            for x in range(len(self.weights)):
                for y in range(len(self.weights[x])):
                    total += c[1][x][y]
                    for z in range(len(self.weights[x][y])):
                        total += c[0][x][y][z]
            if(total < 0):
                total = -total
            if(total == 0):
                total = 1e-256
            for x in range(len(self.weights)):
                for y in range(len(self.weights[x])):
                    self.biases[x][y] -= c[1][x][y] * LearnRate * (avgCost ** 0.5) / total
                    for z in range(len(self.weights[x][y])):
                        self.weights[x][y][z] -= c[0][x][y][z] * LearnRate * (avgCost ** 0.5) / total
            self.CostValue = avgCost
            if self.CostValue < 1e-10:
                break

def biggest(lis):
    big = [0]
    for x in range(len(lis) - 1):
        y = x + 1
        if(lis[y] > lis[big[0]]):
            big = [y]
        if(lis[y] == lis[big[0]] and big[0] != y):
            big.append(y)
    return big[r.randint(0,len(big) - 1)]

def shift(thing, newnum):
    a = thing
    for x in range(len(a) - 1):
        a[x] = a[x + 1]
    a[len(a) - 1] = newnum
    return a

def testseq(feed, sequence, nn):
    james = nn
    score = 0
    future = feed
    for x in range(len(sequence)):
        james.predict(future)
        adversary = 1 * (james.output()[0] > 0.5)
        future = shift(shift(future, sequence[x]), adversary)
        score += table[sequence[x]][adversary]
    return score

def tobinary(num, digits):
    number = num
    bits = []
    for q in range(digits):
        x = digits - q - 1
        if 2 ** x <= number:
            bits.append(1)
            number -= 2 ** x
        else:
            bits.append(0)
    return bits

inittime = t.time()

def strategy(history, memory):
    choice = 1
    tim = t.time()
    if type(memory) == list:
        player = memory[0]
        previousfeed = memory[1]
        wronged = memory[2]
    else:
        player = network([2 * thinklength, 10, 6, 1])
        wronged = False
    feed = []
    for x in range(2 * (thinklength - min(10, len(history[0])))):
        feed.append(0)
    for x in range(min(thinklength, len(history[0]))):
        feed.append(2 * (history[0, x + max(0, len(history[0]) - thinklength)] - 0.5))
        feed.append(2 * (history[1, x + max(0, len(history[0]) - thinklength)] - 0.5))
    if 0 in history[1]:
        wronged = True
    if type(memory) == list and wronged:
        player.predict(previousfeed)
        #if 1 * (player.output()[0] > 0.5) != history[1][len(history[0]) - 1]:
            #print(len(history[0]), 1 * (player.output()[0] > 0.5), history[1][len(history[0]) - 1], "incorrect!")
        player.train(previousfeed, [history[1][len(history[0]) - 1]], LearnRate, LearnIterations)
        #player.train(previousfeed, [history[1][len(history[0]) - 1]], LearnRate, LearnThreshold)
        options = []
        scores = []
        for x in range(2 ** howahead):
            trythis = tobinary(x, howahead)
            options.append(trythis)
            scores.append(testseq(feed, trythis, player))
        choice = options[biggest(scores)][0]
        if len(history[0]) % alert == 1 and alertatall:
            print(player.CostValue)
    if not wronged:
        choice = 1
        #if player.CostValue > 1:
        #    print(t.time() - inittime, "Crap")
    #print(t.time() - tim)
    return choice, [player, feed, wronged]
