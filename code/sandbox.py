


state = {1:2, 3:4, 5:6, 2:8}
actionVals = state
maxVal = max(actionVals, key=actionVals.get)
actionChoice = maxVal

print(actionChoice)