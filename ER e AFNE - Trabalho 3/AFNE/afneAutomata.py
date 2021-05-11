class AFNEAutomata:
    def __init__(self, alphabet, initialState, transitions, acceptingStates):
        self.alphabet = alphabet
        self.initialState = initialState
        self.transitions = transitions
        self.acceptingStates = acceptingStates

    def validateChain(self, chain):
        for i in chain:
            if not i in self.alphabet:
                return False
        return True
