
"""

My solution uses a looker-up algorithm that has been trained
by the Moran process to perform optimally against common
Prisoner's Dilemma strategies.


The algorithm performs as follows:

    looker_up_table = {
        ((C, C), (C, C), (C, C)): C,
        ((C, C), (C, C), (C, D)): D,
        ...
    }

    self_history = (C, C)       <- The last 2 moves of self.

    opponent_history = (C, C)   <- The last 2 moves of opponent.

    opponent_opener = (C, D)    <- The opening 2 moves of opponent.

    next_move = looker_up_table[
    (self_history,
    opponent_history,
    opponent_opener)
    ]                           <- D


The looker-up table contains all possible recent moves for both
opponent and player, along with possible opponent openers.
The pattern (named "pattern" below, creatively) is what determines
what conditions are to be met for the algorithm to choose
Cooperate over Defect.


The Moran process through evolution sometimes leads to
inescapable cooperation, as it's an effective method when
trained against itself. However I have not made any other
evolved looker-up submissions to the competition that would
give me an unfair advantage through utilizing this cooperation.
The effectiveness of the algorithm comes only from it being
trained to perform well against other common algorithms.


Authors Vincent Knight, Marc Harper, Nikoleta E. Gylnatsi,
and Owen Campbell describe this incidental cooperation in
their paper "Evolution reinforces cooperation with the emergence
of self-recognition mechanisms: An empirical study of strategies
in the Moran process for the iterated prisoner’s dilemma" [1].


[1] https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0204981

"""


C, D = 1, 0


def get_lookup_table() -> dict:

    """
    Returns a lookup table for whether the algorithm
    should defect or cooperate based on the previous
    moves done by both the player and the opponent.
    """

    def pad_to(string, length):
        if len(string) < length:
            return ("0"*(length - len(string))) + string
        else:
            return string

    """
    The below pattern is __not__ run in sequence for the
    purpose of handshaking/colluding, but rather used 
    as values to the keys of the previous moves of both 
    the player and the opponent. This is described in 
    more detail above.
    """
    pattern = [
        C, D, D, C, D, C, D, D,
        C, D, D, D, C, D, D, D,
        D, D, C, D, C, D, C, C,
        C, D, D, C, C, D, C, D,
        D, D, C, C, C, C, C, D,
        D, D, C, D, D, D, D, D,
        D, D, D, D, C, C, D, D,
        C, D, D, D, C, C, C, D
    ]

    lookup_str = [pad_to(bin(k)[2:], 6) for k in range(64)][::-1]
    lookup = {
        (
            (int(s[:2][0]), int(s[:2][1])),
            (int(s[2:4][0]), int(s[2:4][1])),
            (int(s[-2:][0]), int(s[-2:][1]))
        ): p for s, p in zip(lookup_str, pattern)
    }
    return lookup


def strategy(history, memory):

    initial_actions = (C, C)

    if not memory:
        memory = get_lookup_table()

    turn_number = history.shape[1]

    if turn_number < 2:

        return initial_actions[turn_number], memory

    else:
        lst_history = list(history)

        self_history = list(lst_history[0])

        opponent_history = list(lst_history[1])

        lookup_reference = (
            tuple(self_history[-2:]),
            tuple(opponent_history[-2:]),
            tuple(opponent_history[:2])
        )

        return memory[lookup_reference], memory
