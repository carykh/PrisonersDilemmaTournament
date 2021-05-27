import numpy as np


################################################################################
###                                                                          ###
###                            OPTIMISTIC THOMAS                             ###
###                                                                          ###
################################################################################
# date: May 2021
# description:
#     Thomas is a strategy for iterated prisoner's dilemma (IPD) tournaments,
#     which uses Bayesian inference [0, 1], to model the probability that it's
#     opponent will defect. It models the probability that the opponent will
#     defect as a beta distribution that is updated between each iteration of
#     the prisoner's dilemma. It use this distribution to test several
#     hypotheses tests and chooses to cooperate or defect according to the
#     outcomes. The Optimistic variation of Thomas is initialized with a beta
#     distribution that assumes the opponent is likely to cooperate.


################################################################################
###                             The Mathematics                              ###
################################################################################


# We need access to the beta function, but since numpy does not define the
# beta function, we must define it ourselves. Unfortunately, numpy also does
# not define the log gamma function, which is the best way I know to
# compute the beta function, so we will have to define that as well.
# I used the Lanczos Approximation to the gamma function [2] and modified it
# to compute the log of the gamma function instead.
def _lanczos_gamma_approximation():
    HALF = 0.5
    PI = np.pi
    LOG_PI = np.log(PI)
    HALF_LOG_2PI = HALF * np.log(2 * PI)
    INIT_Z = 0.99999999999980993227684700473478
    PVALS = [
        676.520368121885098567009190444019,
        -1259.13921672240287047156078755283,
        771.3234287776530788486528258894,
        -176.61502916214059906584551354,
        12.507343278686904814458936853,
        -0.13857109526572011689554707,
        9.984369578019570859563e-6,
        1.50563273514931155834e-7
    ]
    N_PVALS_M1 = len(PVALS) - 1

    def _lgamma(x):
        if x < HALF:
            y = LOG_PI - np.log(np.sin(PI * x)) - _lgamma(1 - x)
        else:
            z = INIT_Z
            for (k, pval) in enumerate(PVALS):
                z += pval / (x + k)
            x_mhalf = x - HALF
            t = x_mhalf + N_PVALS_M1
            y = HALF_LOG_2PI + x_mhalf * np.log(t) - t + np.log(z)
        return y

    return _lgamma

_lgamma = _lanczos_gamma_approximation()


# Here we define the beta function using the log gamma function
# approximation defined above [3]
def _beta(alpha, beta):
    exponent = _lgamma(alpha) + _lgamma(beta) - _lgamma(alpha + beta)
    return np.exp(exponent)


# We use the above mathematical functions to implement a class representing
# a simple beta probability distribution [4]
class _beta_dist:
    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta

    @property
    def mean(self):
        return self.alpha / (self.alpha + self.beta)

    @property
    def std(self):
        numer = np.sqrt(self.alpha * self.beta)
        denom_1 = self.alpha + self.beta
        denom_2 = np.sqrt(denom_1 + 1)
        return numer / (denom_1 * denom_2)

    # Uses Bayesian inference to update distribution [5]
    def update(self, values):
        successes = np.sum(values)
        num_trials = np.prod(np.shape(values))
        self.alpha += successes
        self.beta += num_trials - successes

    def pdf(self, x):
        a = np.power(x, self.alpha - 1)
        b = np.power(1 - x, self.beta - 1)
        return a * b / _beta(self.alpha, self.beta)

    def cdf(self, x, dx=0.01):
        x = np.atleast_1d(x).reshape(-1, 1)
        xs = np.arange(dx, 1 - dx, dx)
        ys = self.pdf(xs)
        integral = np.cumsum(dx * ys, axis=-1)
        integral /= np.max(integral)
        return np.where(xs < x, integral, 0).max(axis=-1)

    def sample(self, size=None):
        return np.random.beta(self.alpha, self.beta, size=size)

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}(alpha={self.alpha}, beta={self.beta})"


################################################################################
###                               Meet Thomas                                ###
################################################################################


class _thomas():
    DEFECT = 0
    COOPERATE = 1

    def __init__(self, alpha0=None, beta0=None, bounds=None):
        self.alpha0 = 1 if alpha0 is None else alpha0
        self.beta0 = 1 if beta0 is None else beta0
        self.bounds = [1/10, 1/3, 2/3, 9/10] if bounds is None else bounds

        self.current_beliefs = _beta_dist(self.alpha0, self.beta0)
        self.significances = np.diff([0, *self.bounds, 1])

    @staticmethod
    def optimistic():
        return _thomas(
            alpha0=1,
            beta0=3
        )

    @staticmethod
    def pessimistic():
        return _thomas(
            alpha0=3,
            beta0=1
        )

    def _random_choice(self, prob_defect):
        # Choose to defect with the same probability with which we belive the
        # opponent will defect.
        rand_num = np.random.random()
        return _thomas.DEFECT if rand_num < prob_defect else _thomas.COOPERATE

    def _get_choice(self, last_move=None):
        # Calculate the p-values for each interval in [0, 1] defined by bounds
        cdf_values = self.current_beliefs.cdf(self.bounds)
        p_values = np.diff([0, *cdf_values, 1])
        p_values /= np.sum(p_values)

        # Reject each interval if the p-value is less than its significance
        rejected = (p_values < self.significances)

        # If we are nearly certain about their next move, then defect
        if all(rejected[1:]) or all(rejected[:-1]):
            return _thomas.DEFECT

        # If we rejected the interval containing 50%, then thomas thinks the
        # opponent is more likely to cooperate than defect or vice versa.
        if rejected[2]:
            # If we don't believe the opponent will defect, then we cooperate
            if rejected[3]:
                return _thomas.COOPERATE
            # If we don't believe the opponent will cooperate, then we defect
            # if rejected[1]: # This is always true since alpha, beta >= 1
            return _thomas.DEFECT

        # Until we can reject the interval containing 50%, play as tit-for-tat
        return last_move

    def choice(self, history):
        # On first turn, just be nice and cooperate
        if history.shape[1] == 0:
            return _thomas.COOPERATE

        # On later turns, update the current beliefs with opponents last move
        last_move = history[1, -1]
        defected = (last_move == _thomas.DEFECT)
        self.current_beliefs.update(defected)

        # get the choice using updated beliefs
        return self._get_choice(last_move)


################################################################################
###                            The Grand Strategy                            ###
################################################################################


def strategy(history, thomas):
    # Wake up Thomas
    thomas = _thomas.optimistic() if thomas is None else thomas

    # Defer to Thomas
    return thomas.choice(history), thomas


################################################################################
###                           Links to References                            ###
################################################################################

# [0] https://en.wikipedia.org/wiki/Bayesian_inference
# [1] https://en.wikipedia.org/wiki/Thomas_Bayes
# [2] https://en.wikipedia.org/wiki/Lanczos_approximation
# [3] https://en.wikipedia.org/wiki/Beta_function
# [4] https://en.wikipedia.org/wiki/Beta_distribution
# [5] http://www.stat.cmu.edu/~larry/=sml/Bayes.pdf
