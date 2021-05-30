def strategy(history, memory):

  #cooperate first turn
  if memory == None:
    return "cooperate", False
    
  #defect if you got defected twice in a row before
  elif memory:
    return "defect", True
    
  else:
  
    #tit for tat
    if history[1,-1] == 0:

      #unless you get defected twice in a row
      if history.shape[1] >= 2 and history[1,-2] == 0:
        return "defect", True
      else:
        return "defect", False
    else:
      return "cooperate", False