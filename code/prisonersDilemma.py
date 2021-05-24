import os, sys
import itertools
import importlib
import numpy as np
import random
from multiprocessing import Queue, Process, freeze_support

STRATEGY_FOLDER = "exampleStrats"
RESULTS_FILE = "results.txt"

# Assumes multithreaded CPU, as such divides by 2, set to zero to prevent spawning of child processes (for debugging and in case of issues in Windows)
PARALLEL_WORKERS = os.cpu_count()//2

pointsArray = [[1,5],[0,3]] # The i-j-th element of this array is how many points you receive if you do play i, and your opponent does play j.
moveLabels = ["D","C"]
# D = defect,     betray,       sabotage,  free-ride,     etc.
# C = cooperate,  stay silent,  comply,    upload files,  etc.


# Returns a 2-by-n numpy array. The first axis is which player (0 = us, 1 = opponent)
# The second axis is which turn. (0 = first turn, 1 = next turn, etc.
# For example, it might have the values
#
# [[0 0 1]       a.k.a.    D D C
#  [1 1 1]]      a.k.a.    C C C
#
# if there have been 3 turns, and we have defected twice then cooperated once,
# and our opponent has cooperated all three times.
def getVisibleHistory(history, player, turn):
    historySoFar = history[:,:turn].copy()
    if player == 1:
        historySoFar = np.flip(historySoFar,0)
    return historySoFar

def strategyMove(move):
    if type(move) is str:
        defects = ["defect","tell truth"]
        return 0 if (move in defects) else 1
    else:
        # Coerce all moves to be 0 or 1 so strategies can safely assume 0/1's only
        return int(bool(move))

def runRound(pair):
    moduleA = importlib.import_module(STRATEGY_FOLDER+"."+pair[0])
    moduleB = importlib.import_module(STRATEGY_FOLDER+"."+pair[1])
    memoryA = None
    memoryB = None
    
    LENGTH_OF_GAME = int(200-40*np.log(1-random.random())) # The games are a minimum of 200 turns long. The np.log here guarantees that every turn after the 200th has an equal (low) chance of being the final turn.
    history = np.zeros((2,LENGTH_OF_GAME),dtype=int)
    
    for turn in range(LENGTH_OF_GAME):
        playerAmove, memoryA = moduleA.strategy(getVisibleHistory(history,0,turn),memoryA)
        playerBmove, memoryB = moduleB.strategy(getVisibleHistory(history,1,turn),memoryB)
        history[0,turn] = strategyMove(playerAmove)
        history[1,turn] = strategyMove(playerBmove)
        
    return history

def runRoundWorker(input_queue, output_queue):
    for pair in iter(input_queue.get, 'STOP'):
        result = runRound(pair)
        output_queue.put( (pair, result) )
    
def tallyRoundScores(history):
    scoreA = 0
    scoreB = 0
    ROUND_LENGTH = history.shape[1]
    for turn in range(ROUND_LENGTH):
        playerAmove = history[0,turn]
        playerBmove = history[1,turn]
        scoreA += pointsArray[playerAmove][playerBmove]
        scoreB += pointsArray[playerBmove][playerAmove]
    return scoreA/ROUND_LENGTH, scoreB/ROUND_LENGTH
    
def outputRoundResults(f, pair, roundHistory, scoresA, scoresB):
    f.write(pair[0]+" (P1)  VS.  "+pair[1]+" (P2)\n")
    for p in range(2):
        for t in range(roundHistory.shape[1]):
            move = roundHistory[p,t]
            f.write(moveLabels[move]+" ")
        f.write("\n")
    f.write("Final score for "+pair[0]+": "+str(scoresA)+"\n")
    f.write("Final score for "+pair[1]+": "+str(scoresB)+"\n")
    f.write("\n")
    
def pad(stri, leng):
    result = stri
    for i in range(len(stri),leng):
        result = result+" "
    return result
    
def runFullPairingTournament(inFolder, outFile):
    print("Starting tournament, reading files from "+inFolder)
    scoreKeeper = {}
    STRATEGY_LIST = []
    for file in os.listdir(inFolder):
        if file.endswith(".py"):
            STRATEGY_LIST.append(file[:-3])
            
    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0
        
    f = open(outFile,"w+")
    pairs = list(itertools.combinations(STRATEGY_LIST, r=2))

    work_queue = Queue()
    done_queue = Queue()
    
    print("Queueing work...")
    for pair in pairs:
        work_queue.put(pair)

    # If we are not using workers then use
    if PARALLEL_WORKERS > 0:
        print("Starting {} workers...".format(PARALLEL_WORKERS))
        for i in range(PARALLEL_WORKERS):
            Process(target=runRoundWorker, args=(work_queue, done_queue)).start()    
    
    # Adds stop flags to the work queue
    for i in range(PARALLEL_WORKERS):
        # since the workers stop when receive a stop flag, we don't wait for them, just for the work results...
        work_queue.put('STOP')

    n_pairs = len(pairs)
    n_round = 0
    for i in range(len(pairs)):
        n_round += 1
        sys.stdout.write("\rRound {} of {}".format(n_round, n_pairs))

        if PARALLEL_WORKERS == 0:
            # Iterative code
            pair = pairs[i]
            roundHistory = runRound(pair)
        else:
            # Parallel code, wait for the workers results
            pair, roundHistory = done_queue.get()    

        scoresA, scoresB = tallyRoundScores(roundHistory)
        outputRoundResults(f, pair, roundHistory, scoresA, scoresB)
        scoreKeeper[pair[0]] += scoresA
        scoreKeeper[pair[1]] += scoresB

    sys.stdout.write("\rRounds done: {}           \n".format(n_round))
        
    scoresNumpy = np.zeros(len(scoreKeeper))
    for i in range(len(STRATEGY_LIST)):
        scoresNumpy[i] = scoreKeeper[STRATEGY_LIST[i]]
    rankings = np.argsort(scoresNumpy)

    f.write("\n\nTOTAL SCORES\n")
    for rank in range(len(STRATEGY_LIST)):
        i = rankings[-1-rank]
        score = scoresNumpy[i]
        scorePer = score/(len(STRATEGY_LIST)-1)
        f.write("#"+str(rank+1)+": "+pad(STRATEGY_LIST[i]+":",16)+' %.3f'%score+'  (%.3f'%scorePer+" average)\n")
        
    f.flush()
    f.close()
    print("Done with everything! Results file written to "+RESULTS_FILE)
    
    
runFullPairingTournament(STRATEGY_FOLDER, RESULTS_FILE)
