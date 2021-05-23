import os
import itertools
import importlib
import numpy as np
import random
from multiprocessing import Pool, cpu_count
from io import StringIO
import statistics
import argparse
import sys
import json

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

parser.add_argument(
    "-s",
    "--strategies",
    dest="strategies",
    nargs="+",
    help="If passed, only these strategies will be tested against each other. If only a single strategy is passed, every other strategy will be paired against it.",
)

parser.add_argument(
    "-j",
    "--num-processes",
    dest="processes",
    type=int,
    default=cpu_count(),
    help="Number of processes to run the simulation with. By default, this is the same as your CPU core count.",
)


args = parser.parse_args()

STRATEGY_FOLDERS = [p for p in os.listdir() if os.path.isdir(p)]
if not args.use_slow:
    STRATEGY_FOLDERS.remove("slow")
RESULTS_FILE = "results.txt"
RESULTS_HTML = "results.html"
RESULTS_JSON = "results.json"
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
        historySoFar = historySoFar[::-1]
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

    # The games are a minimum of 200 turns long. 
    # The np.log here guarantees that every turn after the 200th has an equal (low) chance of being the final turn.
    LENGTH_OF_GAME = int(
        200 - 40 * np.log(1-random.random())
    )
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
    f.write(f"{pair[0]} (P1)  VS.  {pair[1]} (P2)\n")
    for p in range(2):
        for t in range(roundHistory.shape[1]):
            move = roundHistory[p, t]
            f.write(moveLabels[move] + " ")
        f.write("\n")
    f.write(f"Final score for {pair[0]}: {scoresA} ± {stdevA}\n")
    f.write(f"Final score for {pair[1]}: {scoresB} ± {stdevB}\n")
    f.write("\n")


def pad(stri, leng):
    result = stri
    for i in range(len(stri), leng):
        result = result + " "
    return result


def progressBar(width, completion):
    numCompleted = round(width * completion)
    return f"[{'=' * numCompleted}{' ' * (width - numCompleted)}]"


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
    stdevA = statistics.stdev(allScoresA) if len(allScoresA) > 1 else 0
    stdevB = statistics.stdev(allScoresB) if len(allScoresB) > 1 else 0
    outputRoundResults(
        roundResults, pair, firstRoundHistory, scoresA, scoresB, stdevA, stdevB
    )
    roundResults.flush()
    roundResultsStr = roundResults.getvalue()
    roundResults.close()
    return (avgScoreA, avgScoreB, stdevA, stdevB, firstRoundHistory, roundResultsStr)


def runFullPairingTournament(inFolders, outFile, summaryFile):
    print("Starting tournament, reading files from " + ", ".join(inFolders))
    scoreKeeper = {}
    STRATEGY_LIST = []
    for inFolder in inFolders:
        for file in os.listdir(inFolder):
            if file.endswith(".py"):
                STRATEGY_LIST.append(f"{inFolder}.{file[:-3]}")

    if args.strategies is not None and len(args.strategies) > 1:
        STRATEGY_LIST = [strategy for strategy in STRATEGY_LIST if strategy in args.strategies]

    if len(STRATEGY_LIST) < 2:
        raise ValueError('Not enough strategies!')

    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0

    mainFile = open(outFile, "w+")
    summaryFile = open(summaryFile, "w+")

    combinations = list(itertools.combinations(STRATEGY_LIST, r=2))

    if args.strategies is not None and len(args.strategies) == 1:
        combinations = [pair for pair in combinations if pair[0] == args.strategies[0] or pair[1] == args.strategies[0]]

    numCombinations = len(combinations)
    allResults = []
    with Pool(args.processes) as p:
        for i, result in enumerate(
            zip(p.imap(runRounds, combinations), combinations), 1
        ):
            sys.stdout.write(
                f"\r{i}/{numCombinations} pairings ({NUM_RUNS} runs per pairing) {progressBar(50, i / numCombinations)}"
            )
            sys.stdout.flush()
            (
                avgScoreA,
                avgScoreB,
                stdevA,
                stdevB,
                firstRoundHistory,
                roundResultsStr,
            ) = result[0]
            (nameA, nameB) = result[1]
            scoresList = [avgScoreA, avgScoreB]

            allResults.append(
                {
                    "playerA": {
                        "name": nameA,
                        "avgScore": avgScoreA,
                        "stdev": stdevA,
                        "history": list(int(x) for x in firstRoundHistory[0])
                    },
                    "playerB": {
                        "name": nameB,
                        "avgScore": avgScoreB,
                        "stdev": stdevB,
                        "history": list(int(x) for x in firstRoundHistory[1])
                    }
                }
            )
            mainFile.write(roundResultsStr)
            scoreKeeper[nameA] += avgScoreA
            scoreKeeper[nameB] += avgScoreB
    sys.stdout.write("\n")
    sys.stdout.flush()

    with open(RESULTS_JSON, "w+") as j:
        j.write(json.dumps(allResults))

    scoresNumpy = np.zeros(len(scoreKeeper))
    for i in range(len(STRATEGY_LIST)):
        scoresNumpy[i] = scoreKeeper[STRATEGY_LIST[i]]
    rankings = np.argsort(scoresNumpy)
    invRankings = [len(rankings) - int(ranking) - 1 for ranking in np.argsort(rankings)]

    with open("viewer-template.html", "r+") as t:
        jsonStrategies = [
            {
                "name": name,
                "rank": rank,
                "score": score,
                "avgScore": score / (len(STRATEGY_LIST) - 1),
            }
            for (name, rank, score) in zip(STRATEGY_LIST, invRankings, scoresNumpy)
        ]
        jsonResults = json.dumps({"results": allResults, "strategies": jsonStrategies})
        templateStr = t.read()
        with open(RESULTS_HTML, "w+") as out:
            out.write(templateStr.replace("$results", jsonResults))

    mainFile.write("\n\nTOTAL SCORES\n")
    for rank in range(len(STRATEGY_LIST)):
        i = rankings[-1 - rank]
        score = scoresNumpy[i]
        scorePer = score / (len(STRATEGY_LIST) - 1)
        scoreLine = f"#{rank + 1}: {pad(STRATEGY_LIST[i] + ':', 16)}{score:.3f}  ({scorePer:.3f} average)\n"
        mainFile.write(scoreLine)
        summaryFile.write(scoreLine)

    mainFile.flush()
    mainFile.close()
    summaryFile.flush()
    summaryFile.close()
    print("Done with everything! Results file written to " + RESULTS_FILE)


if __name__ == "__main__":
    runFullPairingTournament(STRATEGY_FOLDERS, RESULTS_FILE, SUMMARY_FILE)
