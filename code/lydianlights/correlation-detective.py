import numpy as np

# algorithm: correlation-detective
# by: lydianlights

TRIAL_PERIOD = 10
CERTAINTY_THRESHOLD = 0.8
CORRELATION_THRESHOLD = 0.65
REVENGE_TIMER = 3

# Try to predict whether our stimuli have an effect on the opponent, then try to take advantage
def strategy(history, memory):
  t = history.shape[1]
  if memory == None:
    memory = initMemory()
  
  if t < TRIAL_PERIOD:
    return titForTat(history), memory

  memory = updateMemory(history, memory, t)
  defectPrediction, coopPrediction = calcPredictions(memory, t)

  # we think opponent will coop when we defect -- take full advantage
  if defectPrediction > CERTAINTY_THRESHOLD:
    return 0, memory

  # we think opponent will coop when we coop -- work together unless we have a grudge to settle
  if coopPrediction > CERTAINTY_THRESHOLD:
    if memory["grudge"] > 0 and memory["lastRevengeAt"] > REVENGE_TIMER:
      return 0, memory
    return 1, memory

  # we think opponent will defect on us -- defect in return
  if defectPrediction < -CERTAINTY_THRESHOLD or coopPrediction < -CERTAINTY_THRESHOLD:
    return 0, memory

  # we think the opponent is watching us but we're still unsure of their strategy
  if abs(defectPrediction) > CORRELATION_THRESHOLD or abs(coopPrediction) > CORRELATION_THRESHOLD:
    return titForTat(history), memory

  # we think opponent is unpredictable, so treat them like a random agent
  return 0, memory


# === Memory === #
def initMemory():
  return {
    "grudge": 0,
    "lastRevengeAt": 0,
    "defCausesDef": [],
    "defCausesCoop": [],
    "coopCausesDef": [],
    "coopCausesCoop": [],
  }

def updateMemory(history, memory, t):
  myStimulus = history[0, -2]
  myPrev = history[0, -1]
  oppPrev = history[1, -1]

  if myStimulus == 0:
    if oppPrev == 0:
      memory["defCausesDef"].append(t)
    elif oppPrev == 1:
      memory["defCausesCoop"].append(t)
  elif myStimulus == 1:
    if oppPrev == 0:
      memory["coopCausesDef"].append(t)
    elif oppPrev == 1:
      memory["coopCausesCoop"].append(t)

  if myPrev == 1 and oppPrev == 0:
    memory["grudge"] += 1
  elif myPrev == 0 and oppPrev == 1:
    memory["grudge"] -= 1
    memory["lastRevengeAt"] = t

  return memory


# === Correlations === #
def calcPredictions(memory, t):
  defectSampleSize = len(memory["defCausesDef"]) + len(memory["defCausesCoop"])
  coopSampleSize = len(memory["coopCausesDef"]) + len(memory["coopCausesCoop"])
  correlations = (
    createCorrelation(memory["defCausesDef"], defectSampleSize, t),
    createCorrelation(memory["defCausesCoop"], defectSampleSize, t),
    createCorrelation(memory["coopCausesDef"], coopSampleSize, t),
    createCorrelation(memory["coopCausesCoop"], coopSampleSize, t),
  )

  # Map what we think will happen when we defect/coop to a value -1 to 1
  # -1 means we think they will defect, 1 means we think they will cooperate, 0 means we are unsure
  defectPrediction = correlations[1] - correlations[0]
  coopPrediction = correlations[3] - correlations[2]

  return defectPrediction, coopPrediction

def createCorrelation(positives, sampleSize, t):
  if sampleSize == 0:
    return 0
  
  # Strength of predicted correlations goes down over time, guarding against inconsistency
  strength = 0
  for turnFound in positives:
    turnsAgo = (t + 1) - turnFound
    strength += 1 / turnsAgo
  return len(positives) / sampleSize * np.tanh(strength)


# === Strategies === #
def titForTat(history):
  if history.shape[1] > 0 and history[1, -1] == 0:
    return 0
  return 1
