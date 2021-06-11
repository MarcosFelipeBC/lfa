from PySimpleAutomata import automata_IO
from afneAutomata import AFNEAutomata
from afneProcessScreen import AFNEProcessScreen

def main():
    automataDict = automata_IO.nfa_json_importer("./resources/AFNE.json")

    alphabet = automataDict["alphabet"]

    states = automataDict["states"]

    initialState = ""
    for state in automataDict["initial_states"]:
        initialState = state
        break
    transitions = automataDict["transitions"]

    acceptingState = ""
    for state in automataDict["accepting_states"]:
        acceptingState = state
        break

    automata_IO.nfa_to_dot(automataDict, "AFNE", "./resources")

    automata = AFNEAutomata(alphabet, states, initialState, transitions, acceptingState)

    AFNEProcessScreen(automata)

if __name__ == "__main__":
    main()