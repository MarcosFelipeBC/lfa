from PySimpleAutomata import automata_IO
from automata import Automata
from screen import Screen

def main():
    automataDict = automata_IO.dfa_json_importer("./resources/AFD.json")

    alphabet = automataDict["alphabet"]
    initialState = automataDict["initial_state"]
    transitions = automataDict["transitions"]
    acceptingStates = automataDict["accepting_states"]

    '''Monta a imagem a partir do Json passado'''
    automata_IO.dfa_to_dot(automataDict, "AFD", "./resources")

    automata = Automata(alphabet, initialState, transitions, acceptingStates)
    '''Screen recebe como parametro o caminho da imagem e também o objeto automato'''
    _ = Screen("./resources/AFD.dot.svg", automata)

if __name__ == "__main__":
    main()