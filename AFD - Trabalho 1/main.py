from PySimpleAutomata import automata_IO
from automata import Automata
from screen import Screen

def main():
    automataDict = automata_IO.dfa_json_importer("./resources/automata.json")

    alphabet = automataDict["alphabet"]
    initialState = automataDict["initial_state"]
    transitions = automataDict["transitions"]
    acceptingStates = automataDict["accepting_states"]

    automata_IO.dfa_to_dot(automataDict, "automata", "./resources")

    automata = Automata(alphabet, initialState, transitions, acceptingStates)

    _ = Screen("./resources/automata.dot.svg", automata)

if __name__ == "__main__":
    main()