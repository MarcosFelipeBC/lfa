from PySimpleAutomata import automata_IO
from AFNE.afneAutomata import AFNEAutomata

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

#Construção da árvore de expressão
def buildTree(postfixExpression):
    stack = [None]
    
    for c in postfixExpression:
        cur = Node(c)
        if not c in "*.+":
            stack.append(cur)
        elif c == '*':
            last = stack.pop()
            cur.left = last
            stack.append(cur)
        else:
            last1 = stack.pop()
            last2 = stack.pop()
            cur.right = last1
            cur.left = last2
            stack.append(cur)
    
    return stack.pop()

#Algoritmo de conversão de expressões de infixa para posfixa
#http://www.vision.ime.usp.br/~pmiranda/mac122_2s14/aulas/aula13/aula13.html
def infix2postfix(expression):
    prec = {}
    prec['*'] = 3
    prec['.'] = 2
    prec['+'] = 1
    prec['('] = 0
    stack = ['#']
    postfixExpression = ""
    for c in expression:
        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or c in "abcdefghijklmnopqrstuvwxyz" or c in "0123456789":
            postfixExpression += c
        elif c == '(':
            stack.append(c)
        elif c == ')':
            top = stack[len(stack)-1]
            while top != '#' and top != '(':
                stack.pop()
                postfixExpression += top
                top = stack[len(stack)-1]
            if top == '(':
                stack.pop()
        else:
            while stack[len(stack)-1] != '#' and prec[stack[len(stack)-1]] >= prec[c]:
                postfixExpression += stack.pop()
            stack.append(c)

    while stack[len(stack)-1] != '#':
        postfixExpression += stack.pop()

    return postfixExpression

def mergeConcatenacao(automataLeft: AFNEAutomata, automataRight: AFNEAutomata):
    idx = 0
    conv = {}
    #Adjusting left
    newStates = set()
    for s in sorted(automataLeft.states):
        conv[s] = "q" + str(idx)
        newStates.add(conv[s])
        idx = idx + 1
    automataLeft.states = newStates

    newTransitions = {}
    for (t, symbol) in automataLeft.transitions:
        newDestList = set()
        for dest in automataLeft.transitions[(t, symbol)]:
            newDestList.add(conv[dest])
        newTransitions[(conv[t], symbol)] = newDestList
    automataLeft.transitions = newTransitions

    newAcceptingState = conv[automataLeft.acceptingState]
    automataLeft.acceptingState = newAcceptingState

    newInitialState = conv[automataLeft.initialState]
    automataLeft.initialState = newInitialState

    #Adjusting right
    newStates = set()
    for s in sorted(automataRight.states):
        conv[s] = "q" + str(idx)
        newStates.add(conv[s])
        idx = idx + 1
    automataRight.states = newStates

    newTransitions = {}
    for (t, symbol) in automataRight.transitions:
        newDestList = set()
        for dest in automataRight.transitions[(t, symbol)]:
            newDestList.add(conv[dest])
        newTransitions[(conv[t], symbol)] = newDestList
    automataRight.transitions = newTransitions

    newAcceptingState = conv[automataRight.acceptingState]
    automataRight.acceptingState = newAcceptingState

    newInitialState = conv[automataRight.initialState]
    automataRight.initialState = newInitialState

    #Merging
    newAlphabet = set()
    newAlphabet.update(automataLeft.alphabet)
    newAlphabet.update(automataRight.alphabet)

    newStates = set()
    newStates.update(automataLeft.states)
    newStates.update(automataRight.states)

    newTransitions = {}
    newTransitions.update(automataLeft.transitions)
    newTransitions.update(automataRight.transitions)
    newTransitions[(automataLeft.acceptingState, 'E')] = set([automataRight.initialState])

    newInitialState = automataLeft.initialState

    newAcceptingState = automataRight.acceptingState
    return AFNEAutomata(newAlphabet, newStates, newInitialState, newTransitions, newAcceptingState)


def mergeFechamento(automata: AFNEAutomata):
    idx = 1
    conv = {}
    #Adjusting automata
    newStates = set()
    for s in sorted(automata.states):
        conv[s] = "q" + str(idx)
        newStates.add(conv[s])
        idx = idx + 1
    automata.states = newStates

    newTransitions = {}
    for (t, symbol) in automata.transitions:
        newDestList = set()
        for dest in automata.transitions[(t, symbol)]:
            newDestList.add(conv[dest])
        newTransitions[(conv[t], symbol)] = newDestList
    automata.transitions = newTransitions

    newAcceptingState = conv[automata.acceptingState]
    automata.acceptingState = newAcceptingState

    newInitialState = conv[automata.initialState]
    automata.initialState = newInitialState

    #Adding transitions and states
    newStates = automata.states
    newStates.update(["q0", "q"+str(idx)])

    newTransitions = automata.transitions
    newTransitions[("q0", 'E')] = set([automata.initialState, "q"+str(idx)])
    newTransitions[(automata.acceptingState, 'E')] = set([automata.initialState, "q"+str(idx)])
    
    newInitialState = "q0"

    newAcceptingState = "q"+str(idx)

    return AFNEAutomata(automata.alphabet, newStates, newInitialState, newTransitions, newAcceptingState)


def mergeUniao(automataLeft: AFNEAutomata, automataRight: AFNEAutomata):
    idx = 1
    conv = {}
    #Adjusting left
    newStates = set()
    for state in sorted(automataLeft.states):
        conv[state] = "q" + str(idx)
        newStates.add(conv[state])
        idx = idx + 1
    automataLeft.states = newStates

    newTransitions = {}
    for (t, symbol) in automataLeft.transitions:
        newDestList = set()
        for dest in automataLeft.transitions[(t, symbol)]:
            newDestList.add(conv[dest])
        newTransitions[(conv[t], symbol)] = newDestList
    automataLeft.transitions = newTransitions

    newAcceptingState = conv[automataLeft.acceptingState]
    automataLeft.acceptingState = newAcceptingState

    newInitialState = conv[automataLeft.initialState]
    automataLeft.initialState = newInitialState

    #Adjusting right
    newStates = set()
    for s in sorted(automataRight.states):
        conv[s] = "q" + str(idx)
        newStates.add(conv[s])
        idx = idx + 1
    automataRight.states = newStates

    newTransitions = {}
    for (t, symbol) in automataRight.transitions:
        newDestList = set()
        for dest in automataRight.transitions[(t, symbol)]:
            newDestList.add(conv[dest])
        newTransitions[(conv[t], symbol)] = newDestList
    automataRight.transitions = newTransitions

    newAcceptingState = conv[automataRight.acceptingState]
    automataRight.acceptingState = newAcceptingState

    newInitialState = conv[automataRight.initialState]
    automataRight.initialState = newInitialState

    #Merging
    newAlphabet = set()
    newAlphabet.update(automataLeft.alphabet)
    newAlphabet.update(automataRight.alphabet)

    newStates = set(["q0", "q"+str(idx)])
    newStates.update(automataLeft.states)
    newStates.update(automataRight.states)

    newTransitions = {}
    newTransitions.update(automataLeft.transitions)
    newTransitions.update(automataRight.transitions)
    newTransitions[("q0", 'E')] = set([automataLeft.initialState, automataRight.initialState])
    newTransitions[(automataLeft.acceptingState, 'E')] = set(["q"+str(idx)])
    newTransitions[(automataRight.acceptingState, 'E')] = set(["q"+str(idx)])

    newInitialState = "q0"

    newAcceptingState = "q"+str(idx)
    return AFNEAutomata(newAlphabet, newStates, newInitialState, newTransitions, newAcceptingState)


def buildAutomata(root: Node):
    automata = None
    if root == None:
        alphabet = set()
        initial_state = "q0"
        states = set(["q0"])
        accepting_state = ""
        transitions = {}
        automata = AFNEAutomata(alphabet, states, initial_state, transitions, accepting_state)

    elif root.left == None and root.right == None:
        alphabet = set([root.data])
        initial_state = "q0"

        if root.data == 'E':
            states = set(["q0"])
            accepting_state = "q0"
            transitions = {}
            automata = AFNEAutomata(alphabet, states, initial_state, transitions, accepting_state)   
        else:
            states = set(["q0", "q1"])
            accepting_state = "q1"
            transitions = {("q0", root.data): set(["q1"])}
            automata = AFNEAutomata(alphabet, states, initial_state, transitions, accepting_state)
    elif root.data == '*':
        automataLeft = buildAutomata(root.left)
        automata = mergeFechamento(automataLeft)
    elif root.data == '.':
        automataLeft = buildAutomata(root.left)
        automataRight = buildAutomata(root.right)
        automata = mergeConcatenacao(automataLeft, automataRight)
    else:
        automataLeft = buildAutomata(root.left)
        automataRight = buildAutomata(root.right)
        automata = mergeUniao(automataLeft, automataRight)

    return automata

def main():
    #Leitura da expressão regular na forma infixa
    regularExpression = input()

    #Conversão da expressão regular para a forma posfixa
    postfixExpression = infix2postfix(regularExpression)

    #Construção da árvore de expressão a partir da expressão na forma posfixa
    tree = buildTree(postfixExpression)

    #Construção do AFNE
    automata = buildAutomata(tree)

    #Criação do dicionário requerido pela biblioteca PySimpleAutomata
    automataDict = {
        "alphabet": automata.alphabet,
        "states": automata.states,
        "initial_states": set([automata.initialState]),
        "accepting_states": set([automata.acceptingState]),
        "transitions": automata.transitions
    }

    #Conversão do dicionário de automato para JSON (que será utilizado na execução do AFNE)
    automata_IO.nfa_to_json(automataDict, "AFNE", "./resources")

if __name__ == "__main__":
    main()