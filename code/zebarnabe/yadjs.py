import numpy as np

# Author: José Sousa (zebarnabe@gmail.com)
# 
# YADJS - YADJS is Another Detective by José Sousa
#
# Basically a tactical detective, will analyze the other player responses for exploits
# Defaults to Tit for Tat (Copy-Cat) (unless the oponent is forgiveable)
#
# I'm well aware that this strategy is over-engineered and probably won't win.
# My guess is that some form of simple Tit-for-Tat with some clever form of forgiving will win.
#
# I did my best to optimize the code, but it is still quite an heavy weight, apologies for that.
# Still, if there are people doing Neural Networks and such, this might not be the heaviest you have in your hands.
#
# From what I could tell it is very strong at detecting random behaviours.
# It penalizes (and is penalized by) exploiters like joss or conMan strategies
# Otherwise it tries to get along with cooperable strategies, it won't provoke the opponent more than once
# unless it gets no response
#
# Special cases detected: 
# -----------------------
# Copy-Cat    (Tit for Tat)
# Kitty-Cat   (Forgivable Tit for Tat)
# Greedy      (Always evil, defects, betrays)
# Always Good (Silent)
# Simpleton
# Exploitable forgiveness strategy
# Random
#
# TODO: Greedy search over probabilistic outcome for the next x choices
#       Since this is heavy enough already, for everybody joy I'll skip this implementation idea

# Currently it looks back up to 200 past trades, if you are having some troubles running the tournament
# I can concede to go to only 100 past trades, in my tests my agent will run 20% faster with minimal degradation
# At 75 the gain in performance is minimal when compared with 100 and the results are noticeable worse
LOOKBACK = 200

# This memorizes the results of the calls for a given argument value
def memoize(f):
    results = {}
    def helper(n):
        if n not in results:
            results[n] = f(n)
        return results[n]
    return helper

# Using memoization this shaves a measureable bit of time.
# This function computes some weights applied to summation of the inferences, it is a modified sigmoid curve to give some extra focus in the last 15 trades.
@memoize
def _getWeights(size):
    focus = 15 # Give more weight in the last 15 exchanges
    gamma = 5  # How is the weight slope defined
    return 1 / ( 1 + np.exp( ( -np.arange(1,size+1,1)/size - 1 + focus / size ) * size / 5 ) )

# Creates a cache of the history slices
# This is not being used as it is actually slower, even though we have some hits on the cache (I've tested this), the overhead overwelms the benefits :(
# This was left here as a reference, it teached me a lot about the innards of python and serves as a demonstration of work in my attempts to optimize the code.
class HistoryCache(object):
    __slots__ = ["_history", "_slices", "_hits", "_gets", "__weakref__"]
    def __init__(self, history):
        self._history = history
        self._slices = {}
    def astype(t):
        return self.history.astype(t)
    def __getattribute__(self, name):
        if name in HistoryCache.__slots__:
            return object.__getattribute__(self, name)
        return getattr(object.__getattribute__(self, "_history"), name)
    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_history"), name)
    def __repr__(self):
        return repr(self._history)
    def __getitem__(self, item):
        if isinstance(item, int):
            return self._history[item]
        elif isinstance(item, slice):
            s = (item.start, item.step, item.stop)
            if s not in self._slices:
                v = self._history[item]
                self._slices[s] = v
                return v
            return self._slices[s]
        elif isinstance(item, tuple):
            s = tuple((i.start, i.step, i.stop) if isinstance(i, slice) else i for i in item)
            if s not in self._slices:
                v = self._history[item]
                self._slices[s] = v
                return v
            return self._slices[s]            
        return None
    def __setitem__(self, item, value):
        print("Warning: attempted to set history!")
    def __delitem__(self, item):
        print("Warning: attempted to delete history!")
    def __len__(self):
        return len(self._history)

def _isCopyCat(history):
    weights = _getWeights(history.shape[1]-1)
    return ((history[1,1:] == history[0,:-1]).astype(int)*weights).sum()/weights.sum()

def _isAlwaysEvil(history):
    weights = _getWeights(history.shape[1])
    return ((1-history[1].astype(int))*weights).sum()/weights.sum()
    
def _isAlwaysGood(history):
    weights = _getWeights(history.shape[1])
    return (history[1].astype(int)*weights).sum()/weights.sum()

"""
Forgiveness mechanic of some agents:
 if  -C or C- then cooperate  
     --    D- 
 
This is exploitable:
me:  CDCDCDCDCDC
him: --DCCCDCCCD ... instead of 12 you get 13 points for each 4 trades
"""
def _isForgivingExploitably(history):
    initialized_history = np.concatenate([np.ones((2,2),dtype=int), history], axis=1)
    weights = _getWeights(history.shape[1]-2)
    
    he_cooperates = initialized_history[1,2:]==1
    my_coop_prev1 = initialized_history[0,1:-1]==1
    my_coop_prev2 = initialized_history[0,:-2]==1
    he_def_prev2  = initialized_history[1,:-2]==0
    
    his_expected_coops = (my_coop_prev1 | (my_coop_prev2 & he_def_prev2))
    his_matched_coops = ~np.logical_xor(his_expected_coops, he_cooperates)    

    return (his_matched_coops[2:].astype(int) * weights).sum() / weights.sum()
    
"""
When I defect, he switches output
D- D- C- C-   me
CD DC CC DD   simpleton
"""
def _isSimpleton(history):
    weights = _getWeights(history.shape[1]-1)

    i_defected = history[0,:-1] == 0

    his_prev = history[1,:-1]
    his_curr = history[1,1:]
      
    he_switched = (his_prev != his_curr)
    
    he_switched_ok  = ~np.logical_xor(he_switched, i_defected)
        
    return (he_switched_ok.astype(int) * weights).sum() /weights.sum()

"""
Kitty cat is too forgiving and easily noticeable
Forgives:    Defends:
DCDC         CDD- DDD-   me
CCCC         -CCD --DD   kittycat
"""
def _isKittyCat(history):
    weights = _getWeights(history.shape[1]-3)
    #weightsAll = _getWeights(history.shape[1])

    # Kitty cat forgiving defense
    my_def1_prev3 = (history[0,:-3] == 1)
    my_def1_prev2 = (history[0,1:-2] == 0)
    my_def1_prev1 = (history[0,2:-1] == 0)
    
    his_def1_prev2 = (history[1,1:-2] == 1)
    his_def1_prev1 = (history[1,2:-1] == 1)
    his_def1_curr  = (history[1,3:] == 0)

    # How it is defending
    kitty_cat_defends1 = (my_def1_prev3 & my_def1_prev2 & my_def1_prev1 & his_def1_prev2 & his_def1_prev1 & his_def1_curr)
       
    my_def2_prev3 = ~my_def1_prev3
    my_def2_prev2 = my_def1_prev2
    my_def2_prev1 = my_def1_prev2
    his_def2_prev1 = ~his_def1_prev1
    his_def2_curr  = his_def1_curr
    
    kitty_cat_defends2 = (my_def2_prev3 & my_def2_prev2 & my_def2_prev1 & his_def2_prev1 & his_def2_curr)

    kitty_cat_attacked = his_def1_curr
    
    my_for_prev2 = ~my_def1_prev2 #(history[0,1:-2] == 1)
    my_for_prev1 = my_def1_prev1  #(history[0,2:-1] == 0)
    his_for_curr = ~his_def1_curr #(history[1,3:] == 1)
    
    # How it is forgiving
    kitty_cat_forgives = my_for_prev2 & my_for_prev1 & his_for_curr
    kitty_cat_tackled = my_for_prev1 & ~(kitty_cat_defends1 | kitty_cat_defends2) # tackled but without defending
   
    if (kitty_cat_attacked.astype(int) + kitty_cat_tackled.astype(int)).sum() == 0:
        return 0
   
    return ((kitty_cat_defends1.astype(int) + kitty_cat_defends2.astype(int) + kitty_cat_forgives.astype(int)) * weights).sum() / ((kitty_cat_attacked.astype(int) + kitty_cat_tackled.astype(int)) * weights).sum()
        
def _isForgiveable(history):
    weights = _getWeights(history.shape[1])
    my_evilness, his_evilness = ((history==0).astype(int)*weights).sum(axis=1)
    
    if his_evilness == 0:
        return 2
    
    return my_evilness / his_evilness

def _isVengeful(history):
    weights = _getWeights(history.shape[1]-1)
    pokes = history[0,:-1]==0
    my_pokes      = (pokes.astype(int)*weights).sum()
    his_responses = ((pokes & (history[1,1:]==0)).astype(int)*weights).sum()
    if my_pokes == 0:
        if history[1,:].sum()>0:
            return 1
        else:
            return 0
            
    return his_responses/my_pokes

def _gatherPairs(history, size):
    inputs  = np.array([a[idx:-size+idx] for idx in range(size)])
    outputs = history[1,size:]
    
    pairs = np.append(inputs, [outputs], axis=0)
    
    uniques, counts = np.unique(pairs.T,axis=0, return_counts=True)
    
    return uniques, counts

def _greedySearch(history):
    uniques, counts = _gatherPairs(history, 3)
    # TODO
    moves = []
    probabilities = []
    return moves, probabilities

def _entropy(X):
    unique, count = np.unique(X, return_counts=True, axis=0)
    prob = count/len(X)
    en = np.sum((-1)*prob*np.log2(prob))
    return en
    
def _jointEntropy(Y,X):
    YX = np.c_[Y,X]
    return _entropy(YX)

def _conditionalEntropy(Y,X):
    return _jointEntropy(Y,X) - _entropy(X)

def _isRandom(history):
    # checks for randomness
    if history.shape[1]<5:
        return _entropy(history[1,:])
    elif history.shape[1]<10:
        return _conditionalEntropy(history[1,1:], history[0,:-1])
    elif history.shape[1]<15:
        return _conditionalEntropy(history[1,2:], np.c_[history[0,:-2],history[0,1:-1]])
    else:
        return _conditionalEntropy(history[1,3:], np.c_[history[0,:-3],history[0,1:-2],history[0,2:-1]])

# Since quite often we don't need to compute all the classes this helps a lot with performance
# For the tests I've made having an on-demand computation of them halves the execution time - unless you have a lot of random behaving agents in the pool of strategies
def _inferenceFactory(history):
    inferences_fns = {
        "copycat"     : _isCopyCat,
        "evil"        : _isAlwaysEvil,
        "good"        : _isAlwaysGood,
        "simpleton"   : _isSimpleton,
        "kittycat"    : _isKittyCat,
        "random"      : _isRandom,
        "forgive"     : _isForgiveable,
        "vengeful"    : _isVengeful,
        "exploitable" : _isForgivingExploitably
    }
    
    inferences_memory = {}
    def _getInference(cls):
        if cls not in inferences_memory:
            inferences_memory[cls] = inferences_fns[cls](history)
        return inferences_memory[cls]
    
    _getInference._classes = set(inferences_fns.keys())
    
    return _getInference
        
def strategy(history, memory):
    testingSchedule = [1,0,1,1]
    gameLength = history.shape[1]

    # I tried okay? Using this cache is slower :/
    #history = HistoryCache(history[:,max(-LOOKBACK, -history.shape[1]):])
    history = history[:,max(-LOOKBACK, -history.shape[1]):]
    
    if gameLength == 0:
        memory = {}

    choice = None
    
    if gameLength < 4: # We're still in that initial testing stage.
        if gameLength > 0 and gameLength < 3 and history[1,-1] == 0: 
            choice = 0
        else:
            choice = testingSchedule[gameLength]

    elif gameLength >= 4: # Time to analyze the testing stage and decide what to do based on what the opponent did in that time!
        _getInference = _inferenceFactory(history)

        if _getInference("kittycat") == 1:
            choice = 1-history[0,-1]

        elif _getInference("good") == 1:
            choice = 0

        elif _getInference("evil") == 1:
            choice = 0

        elif _getInference("simpleton") == 1:
            if history[1,-1] == 0 and history[0,-1] == 1:
                choice = 0
            else:
                choice = 1
                
        elif _getInference("copycat") == 1:
            choice = 1
        
        elif "choice" in memory and memory["choice"] == "forgive":
            memory["count"] -= 1
            if memory["count"] == 0 or history[1,-1]==1:
                memory = {}
            choice = 1

        elif _getInference("exploitable")==1:
            choice = 1 - history[0,-1] # Same as kitty cat exploit
        
        elif _getInference("random") >= 0.95 or (max([_getInference(k) for k in _getInference._classes if k not in ["random","forgive", "vengeful"]]) < _getInference("random") and gameLength>15 and _getInference("random") > 0.8):
            choice = 0
        
        elif _getInference("forgive")>1.25 and history[1,-1] == 1:
            choice = 0
            
        elif _getInference("forgive")>0.95 or (_getInference("forgive")>0.90 and history[1,-2] == 1):
            memory["choice"] = "forgive"
            memory["count"]  = 3
            choice = 1 if history[1,-1] == 1 or history[0,-2] == 0 else 0
        else:
            choice = history[1,-1] # Do Tit for Tat

    return choice, memory
