import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import Frame
from tkinter import messagebox
from PIL import Image, ImageTk
from reportlab.graphics.shapes import _DrawTimeResizeable
from reportlab.platypus.doctemplate import SimpleDocTemplate
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
        self.frame_information = tk.Frame(self.root, height=800, width=700, bg='white')
        self.frame_image = tk.Frame(self.root, height=800, width=380, bg='white')
        self.initialWindow()

    def initialWindow(self):
        #self.cleanScreen()
        self.clear_frame(self.frame_information)
        self.clear_frame(self.frame_information)
        
        img = Image.open('./resources/AFNE.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        self.root.geometry("1080x720") 
        yscrollbar = ttk.Scrollbar(self.frame_image, orient= tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill="y")
        canvas = tk.Canvas(self.frame_image,width= 500, height= size[1], bg='white', yscrollcommand = yscrollbar.set)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        yscrollbar.config(command = canvas.yview)
        
        tk.Label(self.frame_information, text="Digite a cadeia a ser consumida", bg='white', font="Verdana 16 bold").place(x= 30, y=10)
        self.frame_information.pack(side=tk.LEFT)
        self.frame_image.pack(side=tk.RIGHT)
        
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

        

        #self.cleanScreen()
        #self.clear_frame(self.frame_information)
        img = Image.open('./resources/AFNE.png')
        pimg = ImageTk.PhotoImage(img)
        size = img.size
        yscrollbar = ttk.Scrollbar(self.frame_image, orient= tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill="y")
        canvas = tk.Canvas(self.frame_image,width= 500, height= size[1], bg='white', yscrollcommand = yscrollbar.set)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=pimg)
        yscrollbar.config(command = canvas.yview)
        
        label = None
        if len(efecho) == 0:
            label = tk.Label(self.frame_information, text=f"ESTADO ATUAL: \"{state}\" | Posição: {position}\nSímbolo: {chain[position]}\nPossibilidades a partir da união dos E-fechos: {{}}", bg='white', font="Verdana 12 bold")
        else:
            label = tk.Label(self.frame_information, text=f"ESTADO ATUAL: \"{state}\" | Posição: {position}\n | Símbolo: {chain[position]}\nPossibilidades a partir da união dos E-fechos: {efecho}", bg='white', font="Verdana 12 bold")
        label.place(x= 10, y= 280)

        self.root.geometry("1080x720")
        self.nextButton(chain)
        self.root.mainloop()
        
    def chainEntry(self):
        chainEntry = tk.StringVar()
        chainEntry = tk.Entry(self.frame_information, width=30, textvariable=chainEntry)
        chainEntry.place(x= 90, y=70)
        return chainEntry

    def nextButton(self, chain): 
        button = tk.Button(self.frame_information, text="Next", command=lambda:self.processingWindow(chain), width=7, height=2)
        button.place(x=170 , y=140)

    def startButton(self, chainEntry):
        button = tk.Button(self.frame_information, text="Start", command=lambda:self.startButtonAction(chainEntry), width=7, height=2)
        button.place(x=170 , y=140)

    def startButtonAction(self, chainEntry):
        chain = chainEntry.get()
        if self.automata.validateChain(chain) == False:
            messagebox.showinfo("Cadeia inválida", "A cadeia possui símbolos inválidos")
            chainEntry.delete(0, 'end')
        else:
            self.processingWindow(chain)

    def endWithSuccess(self, state):
        messagebox.showinfo("Resultado:", "Estado final: " + state + "\nCADEIA ACEITA!")
        self.stack = []
        for state in self.calculateEfecho(self.automata.initialState, set()):
            self.stack.append((state, 0))
        self.initialWindow()

    def endWithFail(self):
        messagebox.showinfo("Resultado:", "CADEIA REJEITADA!")
        self.stack = []
        for state in self.calculateEfecho(self.automata.initialState, set()):
            self.stack.append((state, 0))
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

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

        # Mula mestre: Miguel
        # Rei das Mulas: Lucas

        # (a*.b*)* -> E? sim; cadeia com um único elemento? sim; aaa? sim; abab? sim; ba? sim;

        # Mula maior: 
        # Mula menor: 