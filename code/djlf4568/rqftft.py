# Email: danieljin4568@gmail.com
# Revised version of qftft ("Quarter" Forgiving Tit For Tat)
# Includes random strategy detection (sort of)
# I'd be surprised if this actually works

# "cooperate" = 1, "defect" = 0

def strategy(history, memory):  
  global cCount
  global cRDCount
  choice = None

  if history.shape[1] == 0: # first turn
    cCount = 0
    cRDCount = 0
    choice = "cooperate"
  if history.shape[1] > 1 and history[0,-2] == 1:
    cCount += 1
    if history[1,-1] == 0 and history[0,-2] == 1:
      cRDCount += 1
  
  if history.shape[1] == 0:
    pass
  elif history.shape[1] == 1: # second turn
    if history[1,-1] == 0: # if opp defect last turn
      choice = "defect"
    else:
      choice = "cooperate"
  elif cCount >= 10 and cRDCount / cCount > 0.3: # if detect random
    choice = "defect"
  elif history.shape[1] >= 4 and history[1,0] == 0 and history[1,1] == 0 and history[1,2] == 0 and history[1,3] == 0:
    choice = "defect"
  elif history.shape[1] >= 4 and history[1,0] == 1 and history[1,1] == 1 and history[1,2] == 1 and history[1,3] == 1:
    choice = "cooperate"
  
  else:
    if history[0,-1] == 0: # if i defect last turn
      choice = "cooperate"
    else:
      if history[1,-1] == 0: # if opp defect last turn
        if history[0,-2] == 1: # if i cooperate two turns ago
          choice = "defect"
        else:
          choice = "defect"
      else:
        choice = "cooperate"

  return choice, None
