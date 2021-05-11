import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class AFNEProcessScreen:
    def __init__(self, automata):
        self.getPng("./resources/AFNE.dot.svg")
        self.automata = automata
        self.stack = []
        for state in self.calculateEfecho(self.automata.initialState, set()):
            self.stack.append((state, 0))
        
        self.root = tk.Tk()
        self.initialWindow()

    def initialWindow(self):
        self.cleanScreen()
        self.root.configure(bg='white')
        img = Image.open('./resources/AFNE.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        canvas = tk.Canvas(self.root, width=size[0], height=size[1], bg='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        self.root.geometry("1080x720")

        tk.Label(self.root, text="Digite a cadeia a ser consumida", bg='white', font="Verdana 16 bold", pady=10).place(x=2, y=20)

        chainEntry = self.chainEntry()
        self.startButton(chainEntry)
        self.root.mainloop()

    def calculateEfecho(self, state, efechoSoFar):
        efecho = set([state])
        efechoSoFar.update(efecho)
        if (state, 'E') in self.automata.transitions:
            for nextState in self.automata.transitions[(state, 'E')]:
                if not nextState in efechoSoFar:
                    efecho.update(self.calculateEfecho(nextState, efechoSoFar))
        
        return efecho

    def processingWindow(self, chain):
        print(len(self.stack))
        if len(self.stack) == 0:
            self.endWithFail()
            return 
        
        state, position = self.stack.pop()

        if position == len(chain):
            if state == self.automata.acceptingState:
                self.endWithSuccess(state)
            else: 
                self.processingWindow(chain)
                
        efecho = set()
        if position != len(chain):
            symbol = chain[position]
            if (state, symbol) in self.automata.transitions:
                for nextState in self.automata.transitions[(state, symbol)]:
                    efecho.update(self.calculateEfecho(nextState, set()))

                for nextFromEfecho in efecho:
                    self.stack.append((nextFromEfecho, position+1))

        self.cleanScreen()
        self.root.configure(bg='white') 
        img = Image.open('./resources/AFNE.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        canvas = tk.Canvas(self.root, width=size[0], height=size[1], bg='white')
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        label = None
        if len(efecho) == 0:
            label = tk.Label(self.root, text=f"ESTADO ATUAL: \"{state}\" | Posição: {position} | Símbolo: {chain[position]}\nPossibilidades a partir da união dos E-fechos: {{}}", bg='white', font="Verdana 12 bold")
        else:
            label = tk.Label(self.root, text=f"ESTADO ATUAL: \"{state}\" | Posição: {position} | Símbolo: {chain[position]}\nPossibilidades a partir da união dos E-fechos: {efecho}", bg='white', font="Verdana 12 bold")
        label.pack(side = tk.TOP)

        self.root.geometry("1080x720")
        self.nextButton(chain)
        self.root.mainloop()
        
    def chainEntry(self):
        chainEntry = tk.StringVar()
        chainEntry = tk.Entry(self.root, width=30, textvariable=chainEntry)
        chainEntry.place(x=5, y=90)
        return chainEntry

    def nextButton(self, chain): 
        button = tk.Button(self.root, text="Next", command=lambda:self.processingWindow(chain), width=7, height=2)
        button.place(x=10, y=200)

    def startButton(self, chainEntry):
        button = tk.Button(self.root, text="Start", command=lambda:self.startButtonAction(chainEntry), width=7, height=2)
        button.place(x=10, y=200)

    def startButtonAction(self, chainEntry):
        chain = chainEntry.get()
        if self.automata.validateChain(chain) == False:
            messagebox.showinfo("Cadeia inválida", "A cadeia possui símbolos inválidos")
            chainEntry.delete(0, 'end')
        else:
            self.processingWindow(chain)

    def endWithSuccess(self, state):
        messagebox.showinfo("Resultado:", "Estado final: " + state + "\nCADEIA ACEITA!")
        self.stack = [(self.automata.initialState, 0)]
        self.initialWindow()

    def endWithFail(self):
        messagebox.showinfo("Resultado:", "CADEIA REJEITADA!")
        self.stack = [(self.automata.initialState, 0)]
        self.initialWindow()
    
    def cleanScreen(self):
        _list = self.root.winfo_children()

        for item in _list:
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        for item in _list:
            item.pack_forget()

    def getPng(self, svg_file):
        drawing = svg2rlg(svg_file)
        renderPM.drawToFile(drawing, "./resources/AFNE.png", fmt="PNG")