class AFNEAutomata:
    def __init__(self, alphabet, states, initialState, transitions, acceptingState):
        self.alphabet = alphabet
        self.states = states
        self.initialState = initialState
        self.transitions = transitions
        self.acceptingState = acceptingState

    def validateChain(self, chain):
        for i in chain:
            if not i in self.alphabet:
                return False
        return True

