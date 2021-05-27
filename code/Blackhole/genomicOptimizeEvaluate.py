#Submission by Blackhole (@BlackholeTI) - daniel@hayesclan.co.uk
#This solution defines a policy agent whose gameplay policies are refined using a genetic algorithm based on the existing game history
#The nature of the algorithm means it will run slower than simple policies, but be patient as there are optimizations
#Not sure if this will perform well enough to win, because it can be unreliable. But I had fun! :D

import numpy as np
import random

#Run the strategy
def strategy(history, memory):
    #The algorithm will always cooperate during the first round so as not to trigger retaliations off the bat
    if(len(history[0]) == 0):
        return 1, None
    else:
        #Optimization tournament will be run at the start of the game or if the agent performance seems to be decreasing
        if len(history[0]) <= 20 or determineDegredation(history, memory):
            bestAgent = autoTournament(history, memory)
            choice = bestAgent.calcChoice(history)
            #print("Choice " + str(choice))
            return choice, bestAgent
        else:
            bestAgent = memory
            choice = bestAgent.calcChoice(history)
            #print("Choice " + str(choice))
            return choice, bestAgent

#Rewards are altered as the algorithm performs better if it values cooperation to ensure high average results. Individual match win priorities do not perform best on a tournament level
pointsArray = [[1,5],[0,6]]

#The algorithm runs its own tournament on the game history and trains the best solution using random initialization and genetic refinement
def autoTournament(history, memory):
    if len(history[0]) > 20:
        reallen = len(history[0])
        history = [history[0][reallen - 20:-1], history[1][reallen - 20:-1]]
    #Higher populations mean better results. I limited it a little so as to not result in extremely long wait times
    #If this runs too slowly, the number can be lowered. But for the solution's sake, please try not to nerf it!
    population = 500
    agents = []
    if memory == None:
        for i in range(population):
            a = Agent()
            a.initGenes()
            agents.append(a)
    else:
        oldStrat = memory.clone()
        for i in range(population):
            if(i < population/2):
                agents.append(oldStrat.clone())
            else:
                a = Agent()
                a.initGenes()
                agents.append(a)
    # Sometimes the initial solution spread is enough variety, but sometimes a small number of generations are needed
    # Here I used 6
    generations = 6
    mutationRate = 0.05
    for gen in range(generations):
        #print("Generation " + str(gen))
        agentScores = [0] * population
        for i, agent in enumerate(agents):
            score = 0
            for round in range(len(history[0])):
                personalHistory = [history[0][0:round], history[1][0:round]]
                choice = agent.calcChoice(personalHistory)
                opponentChoice = history[1][round]
                score += pointsArray[choice][opponentChoice]
            avrScore = score/len(history[0])
            agentScores[i] = avrScore
        sortableAgents = [(agent, agentScores[i]) for i, agent in enumerate(agents)]
        sortedAgents = sorted(sortableAgents, key=lambda agent: agent[1])
        agents = [agent[0] for agent in sortedAgents]
        #Breed
        children = []
        for i in range(0, int(population / 2)):
            parent1 = agents[population - random.randint(1, random.randint(1, population) + 1)]
            parent2 = agents[population - random.randint(1, random.randint(1, population) + 1)]
            childWeightGenome = np.zeros(11)
            childThresholdGenome = np.zeros(8)
            #Mutate
            for w in range(11):
                childWeightGenome[w] = random.choice([parent1.weightGenome[w], parent2.weightGenome[w]])
                if random.random() < mutationRate:
                    childWeightGenome[w] = np.random.uniform(-1, 1)
            for t in range(8):
                childThresholdGenome[t] = random.choice([parent1.thresholdGenome[t], parent2.thresholdGenome[t]])
                if random.random() < mutationRate:
                    childThresholdGenome[t] = random.random()
        for i, child in enumerate(children):
            agents[i] = child
        #print(sortedAgents[-1][1])
    return agents[population - 1]

#Determines if the last agent decreased average performance
def determineDegredation(history, memory):
    retainedAgent = memory
    score = 0
    lastScore = 0
    for round in range(len(history[0])):
        personalHistory = [history[0][0:round], history[1][0:round]]
        choice = retainedAgent.calcChoice(personalHistory)
        opponentChoice = history[1][round]
        if round == (len(history[0]) - 1):
            lastScore = score
        score += pointsArray[choice][opponentChoice]
    avrScore = score / len(history[0])
    lastAvrScore = lastScore / (len(history[0]) - 1)
    return avrScore < lastAvrScore

#Factor list:
#LastOpponentCoop, LastOpponentDefect, LastPlayerCoop, LastPlayerDefect, AverageOpponentCoop, AverageOpponentDefect, AveragePlayerCoop, AveragePlayerDefect, DefaultTendency, DefaultWeight, RandomWeight
#Thresholds for the first 8 tests to trigger allow more complex behavior

#Policy agent class
class Agent:
    def __init__(self):
        self.weightGenome = np.zeros(11)
        self.thresholdGenome = np.zeros(8)
    def initGenes(self):
        self.thresholdGenome = np.random.uniform(0, 1, np.shape(self.thresholdGenome))
        self.weightGenome = np.random.uniform(-1, 1, np.shape(self.weightGenome))
    def set(self, newWeightG, newThreshG):
        self.weightGenome = newWeightG
        self.thresholdGenome = newThreshG
    def clone(self):
        cloned = Agent()
        cloned.set(self.weightGenome, self.thresholdGenome)
        return cloned
    def calcChoice(self, history):
        totalPlayerCoop = 0
        totalOpponentCoop = 0
        for i in history[0]:
            totalPlayerCoop += i
        averagePC = 0
        averagePD = 0
        if(len(history[0]) > 0):
            averagePC = float(totalPlayerCoop) / len(history[0])
            averagePD = 1 - averagePC
        averageOC = 0
        averageOD = 0
        for i in history[1]:
            totalOpponentCoop += i
        if (len(history[0]) > 0):
            averageOC = float(totalOpponentCoop) / len(history[1])
            averageOD = 1 - averageOC
        lastPC = 0
        lastOC = 0
        if (len(history[0]) > 0):
            lastPC = history[0][-1]
            lastOC = history[1][-1]
        inputs = [lastOC, 1 - lastOC, lastPC, 1 - lastPC, averageOC, averageOD, averagePC, averagePD]
        response = 0
        for i, param in enumerate(inputs):
            if not param < self.thresholdGenome[i]:
                response += (param * self.weightGenome[i])
        response = response + (self.weightGenome[8] * self.weightGenome[9]) + (self.weightGenome[10] * random.uniform(-1, 1))
        if response >= 0:
            return 1
        else:
            return 0


