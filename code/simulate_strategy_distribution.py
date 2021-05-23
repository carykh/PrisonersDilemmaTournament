#!/usr/bin/env python


''' Reads a results.txt file which was output by prisonersDilemma.py
    and simulates what the rankings would be if there were many agents
    with different strategy distributions across the agents
'''


import pprint
import pathlib


RESULTS_FILE_PATH = pathlib.Path("results.txt").absolute()

# Within a given distribution, strats that aren't mentioned have equal weight to each other and sum up to 1
STRATEGY_DISTRIBUTIONS = [
    {"exampleStrats.titForTat": 4},  # 80% of agents use a tft strat
    {"exampleStrats.random": 3},     # 75% of agents use a random strat
    {"exampleStrats.titForTat": 2, "exampleStrats.random": 1},
    {"exampleStrats.titForTat": 1, "exampleStrats.random": 1, "exampleStrats.ftft": 0.5}
]


def main():
    matchups_dict, strategy_names = parse_results_file()
    for distribution in STRATEGY_DISTRIBUTIONS:
        simulate_strategy_distribution(matchups_dict, strategy_names, distribution)


def parse_results_file():
    with open(RESULTS_FILE_PATH) as f:
        content = f.readlines()

    final_scores = []
    for line in content:
        if line.startswith("Final score for"):
            final_scores.append(line.strip())

    matchups_dict = {}  # Maps a normalized strategy matchup pair name, to the final scores for the match up
    strategy_names = set()
    for i in range(len(final_scores) - 1):
        name_a, score_a = _parse_final_score(final_scores[i])
        name_b, score_b = _parse_final_score(final_scores[i + 1])
        strategy_names.add(name_a)
        strategy_names.add(name_b)

        matchup_name, first_score, second_score = _get_matchup_entry(name_a, name_b, score_a, score_b)
        matchups_dict[matchup_name] = (first_score, second_score)

    return matchups_dict, strategy_names


def _parse_final_score(line):
    strategy_name = line.split(" ")[3][:-1]
    score = line.split(" ")[4]
    return strategy_name, score


def _get_matchup_entry(name_a, name_b, score_a, score_b):
    if name_a < name_b:
        return name_a + " vs. " + name_b, score_a, score_b
    elif name_b < name_a:
        return name_b + " vs. " + name_a, score_b, score_a
    else:
        raise Exception(f"Found 2 strategies, {name_a} and {name_b} that are the same")


def simulate_strategy_distribution(matchups_dict, strategy_names, distribution):
    total_scores = {}
    for strategy_name in strategy_names:
        total_scores[strategy_name] = 0

    strategy_weights = _get_strategy_weights(strategy_names, distribution)

    for matchup, scores in matchups_dict.items():
        name_a = matchup.split(" ")[0]
        name_b = matchup.split(" ")[2]
        total_scores[name_a] += strategy_weights[name_b] * float(scores[0])
        total_scores[name_b] += strategy_weights[name_a] * float(scores[1])

    rankings = sorted(((v,k) for k,v in total_scores.items()), reverse=True)

    pprint.pp(rankings)
    print()
            

# Returns a dict representing the a normalized weight vector of all the strategies given
def _get_strategy_weights(strategy_names, distribution):
    strategy_weights = distribution.copy()
    default_weight = 1 / (len(strategy_names) - len(distribution))

    for name in strategy_weights:
        if not name in strategy_names:
            raise Exception(f"The given name {name} does not exist in results.txt")

    for strategy_name in strategy_names:
        if not strategy_name in strategy_weights:
            strategy_weights[strategy_name] = default_weight

    total_weight = 0
    for strategy_weight in strategy_weights.values():
        total_weight += strategy_weight

    print(f"Distribution is {distribution}")
    print(f"Total weight for distribution is {total_weight}")

    for strategy_name in strategy_weights:
        strategy_weights[strategy_name] = strategy_weights[strategy_name] / total_weight

    print("Normalized weights vector:")
    pprint.pp(strategy_weights)

    return strategy_weights


if __name__ == "__main__":
    main()
