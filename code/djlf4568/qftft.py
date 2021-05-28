# email: danieljin4568@gmail.com
# discord: DJLF#6985

def strategy(history, memory):
  # "cooperate" = 1, "defect" = 0
  choice = None
  if history.shape[1] == 0: # first turn
    choice = "cooperate"
  elif history.shape[1] == 1: # second turn
    if history[1,-1] == 0: # if opp defect last turn
      choice = "defect"
    else:
      choice = "cooperate"
  elif history.shape[1] >= 4 and history[1,0] == 0 and history[1,1] == 0 and history[1,2] == 0 and history[1,3] == 0:
    choice = "defect"
  elif history.shape[1] >= 4 and history[1,0] == 1 and history[1,1] == 1 and history[1,2] == 1 and history[1,3] == 1:
    choice = "cooperate"

  else: # not first or second turn
    if history[0,-1] == 0: # if i defect last turn
      choice = "cooperate"
    else: # if i cooperate last turn
      if history[1,-1] == 0: # if opp defect last turn
        if history[0,-2] == 1: # if i cooperate two turns ago
          choice = "defect"
        else: # if i defect two turns ago
          choice = "defect"
      else: # if opp cooperate last turn
        choice = "cooperate"

  return choice, None
