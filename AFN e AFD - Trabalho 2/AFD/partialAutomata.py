import json
from automata import Automata
from PySimpleAutomata import automata_IO

class PartialAutomata:
    def __init__(self, automata):
        self.completeAutomata = automata
        self.partialAlphabet = set()
        self.partialStates = {automata.initialState}
        self.partialTransitions = {}
        self.partialAcceptingStates = set()
        if automata.initialState in automata.acceptingStates:
            self.partialAcceptingStates.add(automata.initialState)
        self.currentState = automata.initialState

    def consumeChain(self, chain, position):
        self.nextStep(chain[position])
        self.createImage()

    def nextStep(self, symbol):
        nextState = self.completeAutomata.getNextState(self.currentState, symbol)
        self.addMissingParts(nextState, symbol)
        self.currentState = nextState

    def createImage(self):
        data = {
            'alphabet': self.partialAlphabet,
            'states': self.partialStates,
            'initial_state': self.completeAutomata.initialState,
            'accepting_states': self.partialAcceptingStates,
            'transitions': self.partialTransitions
        }
    
        automata_IO.dfa_to_dot(data, "partialAutomata", "./resources")

    '''
    Função AddMissingParts: 

     Verifica se o próixmo estado não dentro de estados parciais, se verdadeiro, então atribui a estados parciais esse próximo estado e verifica se o próximo estado faz parte de um conjunto de estados aceitos, se sim insere em estados aceitos parciais.

     Por fim cria um transição a partir desse estado e coloca no conjunto de transições parciais.

     Depois verifica se o symbolo pertence ao alfabeto, se sim adiciona ele ao conjunto do alfabeto

    '''
    def addMissingParts(self, nextState, symbol):
        if not nextState in self.partialStates:
            self.partialStates.add(nextState)
            if nextState in self.completeAutomata.acceptingStates:
                self.partialAcceptingStates.add(nextState)
        
        self.partialTransitions[(self.currentState, symbol)] = nextState

        if not symbol in self.partialAlphabet:
            self.partialAlphabet.add(symbol)
