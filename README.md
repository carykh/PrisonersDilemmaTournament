# PrisonersDilemmaTournament

This is my CS 269i class project.

Watch This Place's awesome videos about iterated Prisoner's Dilemma for context!

https://www.youtube.com/watch?v=t9Lo2fgxWHw

https://www.youtube.com/watch?v=BOvAbjfJ0x0

Nicky Case's "The Evolution of Trust" is also super fascinating, but it's not necessary to understand this project: https://ncase.me/trust/

How this works:
When you run code/prisonersDilemma.py, it will search through all the Python strategy files in code/exampleStrats. Then, it will simulate "Iterated Prisoner's Dilemma" with every possible pairing. (There are (n choose 2) pairings.) After all simulations are done, it will average each strategies' overall score. It will then produce a leaderboard of strategies based on their average performance, and save it to results.txt.

If you'd like to add your own strategy, all you have to do is create a new .py file in the code/exampleStrats folder that follows the same format as the others. Then, when you run code/prisonersDilemma.py, it should automatically include your strategy into the tournament!

# Details
| Payout Chart  | Player A cooperates | Player A defects |
| ------------- | ------------- | ------------- |
| Player B cooperates  | A: +3, B: +3  | A: +5, B: +0  |
| Player B defects  | A: +0, B: +5  | A: +1, B: +1  |

In this code, 0 = 'D' = defecting, and 1 = 'C' = cooperating.

---

Strategy functions take in two parameters, 'history' and 'memory', and output two values: 'moveChoice' and 'memory'. 'history' is a 2\*n numpy array, where n is the number of turns so far. Axis one corresponds to "this player" vs "opponent player", and axis two corresponds to what turn number we're on.
For example, it might have the values
```
 [[0 0 1]       a.k.a.    D D C
  [1 1 1]]      a.k.a.    C C C
```
In this case, there have been 3 turns, we have defected twice then cooperated once, and our opponent has cooperated all three times.

'memory' is a very open-ended parameter that can takes on any information that should be retained, turn-to-turn. Strategies that don't need memory, like Tit-for-tat, can simply return None for this variable. If you want to keep track of being 'wronged', like grimTrigger.py, you can set memory to True or False. If you have an extremely complicated strategy, you have make 'memory' store a list of arbitrarily many varibles!

For the outputs: the first value is just the move your strategy chooses to make, with 0 being defect and 1 being cooperate. The second value is any memory you'd like to retain into the next iteration. This can be 'None'.

---

Each pairing simulation runs for this many turns:
```
200-40*np.log(random.random())
```
This means each game is guaranteed to be at least 200 turns long. But then, for every turn after the 200th, there is an equal probability that the game ends. The probability is very low, so there should be no strategizing to defect on the very last turn consequence-free.
