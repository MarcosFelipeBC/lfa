from PySimpleAutomata import automata_IO
from afneAutomata import AFNEAutomata
from afneProcessScreen import AFNEProcessScreen

def main():
    automataDict = automata_IO.nfa_json_importer("./resources/AFN.json")

    alphabet = automataDict["alphabet"]
    initialState = ""
    for state in automataDict["initial_states"]:
        initialState = state
        break
    transitions = automataDict["transitions"]

    acceptingStates = automataDict["accepting_states"]

    automata_IO.nfa_to_dot(automataDict, "AFN", "./resources")

    automata = AFNEAutomata(alphabet, initialState, transitions, acceptingStates)

    AFNEProcessScreen(automata)

if __name__ == "__main__":
    main()