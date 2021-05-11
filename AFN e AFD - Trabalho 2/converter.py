from PySimpleAutomata import automata_IO

AFDStates = set()
AFDTransitions = {}
AFDAlphabet = set()
AFDInitialState = set()
AFDAcceptingStates = set()

statesMap = {}

def buildTransitions(stateSet, AFNTransitions, AFNAcceptingStates):
    global AFDAcceptingStates
    global AFDStates

    for symbol in AFDAlphabet:
        nextStateSet = set()
        for state in stateSet:
            if (state, symbol) in AFNTransitions:
                nextStateSet = nextStateSet.union(AFNTransitions[(state, symbol)])

        AFDTransitions[(getStateString(stateSet), symbol)] = getStateString(nextStateSet)

        if not getStateString(nextStateSet) in AFDStates:
            if len(AFNAcceptingStates.intersection(nextStateSet)) != 0:
                AFDAcceptingStates.add(getStateString(nextStateSet))
            AFDStates.add(getStateString(nextStateSet))
            buildTransitions(nextStateSet, AFNTransitions, AFNAcceptingStates)

def getStateString(stateSet):
    stateString = "|"
    for state in sorted(stateSet):
        stateString += state + "|"
        
    return stateString

def mapStates():
    cnt = 1
    statesMap[getStateString(AFDInitialState)] = "s0"
    for state in AFDStates:
        if state == getStateString(AFDInitialState): 
            continue
        
        statesMap[state] = "s" + str(cnt)
        cnt += 1

def afdStates():
    afdStates = set(["s0"])
    for state in AFDStates:
        afdStates.add(statesMap[state])
    
    return afdStates

def afdAcceptingStates():
    afdAcceptingStates = set()
    for state in AFDAcceptingStates:
        afdAcceptingStates.add(statesMap[state])

    return afdAcceptingStates

def afdTransitions():
    afdTransitions = {}
    for (state, symbol), value in AFDTransitions.items():
    
        newNextState = statesMap[value]

        afdTransitions[(statesMap[state], symbol)] = newNextState

    return afdTransitions


def main():
    global AFDStates
    global AFDTransitions
    global AFDAcceptingStates
    global AFDAlphabet
    global AFDInitialState

    automataDict = automata_IO.nfa_json_importer("./resources/AFN.json")

    alphabet = automataDict["alphabet"]
    initialState = ""
    for state in automataDict["initial_states"]:
        initialState = state
        break
    transitions = automataDict["transitions"]
    acceptingStates = automataDict["accepting_states"]

    AFDInitialState = set([initialState])
    AFDAlphabet = alphabet
    buildTransitions(AFDInitialState, transitions, acceptingStates)

    mapStates()

    AFD = {
            'alphabet': AFDAlphabet,
            'states': afdStates(),
            'initial_state': "s0",
            'accepting_states': afdAcceptingStates(),
            'transitions': afdTransitions()
        }

    automata_IO.dfa_to_json(AFD, "AFD", "./resources")

if __name__ == "__main__":
    main()