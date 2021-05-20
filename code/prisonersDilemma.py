import os
import itertools
import importlib
import numpy as np
import random
from multiprocessing import Pool
from io import StringIO
import statistics
import argparse
import sys

parser = argparse.ArgumentParser(description="Run the Prisoner's Dilemma simulation.")
parser.add_argument(
    "-n",
    "--num-runs",
    dest="num_runs",
    type=int,
    default=100,
    help="Number of runs to average out",
)

parser.add_argument(
    "--skip-slow",
    dest="use_slow",
    action="store_false",
    help="Skip slow strategies for better performance",
)

args = parser.parse_args()

STRATEGY_FOLDERS = ["exampleStrats", "valadaptive", "nekiwo", "edward", "misc", "etc"]
if args.use_slow:
    STRATEGY_FOLDERS.append("slow")
RESULTS_FILE = "results.txt"
SUMMARY_FILE = "summary.txt"
NUM_RUNS = args.num_runs

pointsArray = [
    [1, 5],
    [0, 3],
]  # The i-j-th element of this array is how many points you receive if you do play i, and your opponent does play j.
moveLabels = ["D", "C"]
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
    historySoFar = history[:, :turn].copy()
    if player == 1:
        historySoFar = np.flip(historySoFar, 0)
    return historySoFar


def strategyMove(move):
    if type(move) is str:
        defects = ["defect", "tell truth"]
        return 0 if (move in defects) else 1
    else:
        return move


def runRound(pair):
    moduleA = importlib.import_module(pair[0])
    moduleB = importlib.import_module(pair[1])
    memoryA = None
    memoryB = None

    LENGTH_OF_GAME = int(
        200 - 40 * np.log(random.random())
    )  # The games are a minimum of 50 turns long. The np.log here guarantees that every turn after the 50th has an equal (low) chance of being the final turn.
    history = np.zeros((2, LENGTH_OF_GAME), dtype=int)

    for turn in range(LENGTH_OF_GAME):
        playerAmove, memoryA = moduleA.strategy(
            getVisibleHistory(history, 0, turn), memoryA
        )
        playerBmove, memoryB = moduleB.strategy(
            getVisibleHistory(history, 1, turn), memoryB
        )
        history[0, turn] = strategyMove(playerAmove)
        history[1, turn] = strategyMove(playerBmove)

    return history


def tallyRoundScores(history):
    scoreA = 0
    scoreB = 0
    ROUND_LENGTH = history.shape[1]
    for turn in range(ROUND_LENGTH):
        playerAmove = history[0, turn]
        playerBmove = history[1, turn]
        scoreA += pointsArray[playerAmove][playerBmove]
        scoreB += pointsArray[playerBmove][playerAmove]
    return scoreA / ROUND_LENGTH, scoreB / ROUND_LENGTH


def outputRoundResults(f, pair, roundHistory, scoresA, scoresB, stdevA, stdevB):
    f.write(pair[0] + " (P1)  VS.  " + pair[1] + " (P2)\n")
    for p in range(2):
        for t in range(roundHistory.shape[1]):
            move = roundHistory[p, t]
            f.write(moveLabels[move] + " ")
        f.write("\n")
    f.write(
        "Final score for " + pair[0] + ": " + str(scoresA) + " ± " + str(stdevA) + "\n"
    )
    f.write(
        "Final score for " + pair[1] + ": " + str(scoresB) + " ± " + str(stdevB) + "\n"
    )
    f.write("\n")


def pad(stri, leng):
    result = stri
    for i in range(len(stri), leng):
        result = result + " "
    return result


def progressBar(width, completion):
    numCompleted = round(width * completion)
    return "[" + ("=" * numCompleted) + (" " * (width - numCompleted)) + "]"


def runRounds(pair):
    roundResults = StringIO()
    allScoresA = []
    allScoresB = []
    firstRoundHistory = None
    for i in range(NUM_RUNS):
        roundHistory = runRound(pair)
        scoresA, scoresB = tallyRoundScores(roundHistory)
        if i == 0:
            firstRoundHistory = roundHistory
        allScoresA.append(scoresA)
        allScoresB.append(scoresB)
    avgScoreA = statistics.mean(allScoresA)
    avgScoreB = statistics.mean(allScoresB)
    stdevA = statistics.stdev(allScoresA)
    stdevB = statistics.stdev(allScoresB)
    outputRoundResults(
        roundResults, pair, firstRoundHistory, scoresA, scoresB, stdevA, stdevB
    )
    roundResults.flush()
    roundResultsStr = roundResults.getvalue()
    roundResults.close()
    return (avgScoreA, avgScoreB, roundResultsStr)


def runFullPairingTournament(inFolders, outFile, summaryFile):
    print("Starting tournament, reading files from " + ", ".join(inFolders))
    scoreKeeper = {}
    STRATEGY_LIST = []
    for inFolder in inFolders:
        for file in os.listdir(inFolder):
            if file.endswith(".py"):
                STRATEGY_LIST.append(inFolder + "." + file[:-3])

    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0

    mainFile = open(outFile, "w+")
    summaryFile = open(summaryFile, "w+")

    combinations = list(itertools.combinations(STRATEGY_LIST, r=2))
    numCombinations = len(combinations)
    with Pool() as p:
        for i, result in enumerate(
            zip(p.imap(runRounds, combinations), combinations), 1
        ):
            sys.stdout.write(
                f"\r{i}/{numCombinations} pairings ({NUM_RUNS} runs per pairing) {progressBar(50, i / numCombinations)}"
            )
            sys.stdout.flush()
            (avgScoreA, avgScoreB, roundResultsStr) = result[0]
            (nameA, nameB) = result[1]
            mainFile.write(roundResultsStr)
            scoreKeeper[nameA] += avgScoreA
            scoreKeeper[nameB] += avgScoreB
    sys.stdout.write("\n")
    sys.stdout.flush()

    scoresNumpy = np.zeros(len(scoreKeeper))
    for i in range(len(STRATEGY_LIST)):
        scoresNumpy[i] = scoreKeeper[STRATEGY_LIST[i]]
    rankings = np.argsort(scoresNumpy)

    mainFile.write("\n\nTOTAL SCORES\n")
    for rank in range(len(STRATEGY_LIST)):
        i = rankings[-1 - rank]
        score = scoresNumpy[i]
        scorePer = score / (len(STRATEGY_LIST) - 1)
        scoreLine = (
            "#"
            + str(rank + 1)
            + ": "
            + pad(STRATEGY_LIST[i] + ":", 16)
            + " %.3f" % score
            + "  (%.3f" % scorePer
            + " average)\n"
        )
        mainFile.write(scoreLine)
        summaryFile.write(scoreLine)

    mainFile.flush()
    mainFile.close()
    summaryFile.flush()
    summaryFile.close()
    print("Done with everything! Results file written to " + RESULTS_FILE)


if __name__ == "__main__":
    runFullPairingTournament(STRATEGY_FOLDERS, RESULTS_FILE, SUMMARY_FILE)
